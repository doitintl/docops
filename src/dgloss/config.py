import ast
import os
import re
import pathlib
from collections import UserDict

import nltk
from nltk import downloader
from nltk import stem
from nltk.corpus import stopwords

from tabulate import tabulate
import inflection
import inflect

import dgloss
from dgloss import charset
from dgloss.print import Printer
from dgloss.cache import Cache


# TODO: Change to Command?
class Instruction:

    _filename = None
    _line_num = None

    _command_name = None
    _option_name = None
    _argument = None

    _command = None
    _option = None

    def __init__(self, filename, line_num):
        self.filename = filename
        self.line_num = line_num


class Configuration(UserDict):

    # TODO: Add more corpora to test with
    # TODO: Allow users to select which corpora to use
    # TODO: Document this in the CLI script
    PKG_WORD_FREQ_CORPORA = [
        {
            "name": "leeds",
            "data_filename": "corpora/leeds.txt.gz",
            "re": r"(?P<rank>\d+) +(?P<ipm>\d+(\.?\d+)) +(?P<lemma>\w+)",
        }
    ]

    # https://www.nltk.org/nltk_data/
    NLTK_CORPORA = ["punkt", "wordnet", "stopwords"]

    target_dirname = None
    config_dirname = None

    printer = None
    cache = None
    word_freq_corpus = None
    lemmatizer = None

    ignore_case = True
    ignore_literals = set()
    ignore_regexes = set()

    # Expected format for entries in this list: `[filename, line_num, msg]`
    _parse_errors = []

    def __init__(self, target_dirname, config_dirname):
        # If the user invoked the program that didn't require `DIR` to be set,
        # this value will be None
        if target_dirname:
            self.target_dirname = pathlib.Path(target_dirname)
        if config_dirname:
            self.config_dirname = pathlib.Path(config_dirname)
        else:
            # If no config directory is specified, default to searching the
            # target directory for configuration files
            self.config_dirname = pathlib.Path(target_dirname)
        self.printer = Printer()
        self.cache = Cache()

    def _print(self, *args):
        self.printer.print(*args)

    def load(self):
        self._init_nltk()
        self._scan_dir()

    def _init_nltk(self):
        cache_path = self.cache.get_cache_path()
        nltk_dir = cache_path.joinpath("nltk")
        nltk_dir.mkdir(parents=True, exist_ok=True)
        nltk.data.path.insert(0, nltk_dir)
        dl = downloader.Downloader()
        for name in self.NLTK_CORPORA:
            if not dl.is_installed(name):
                if not dgloss.quiet:
                    self._print(f"<fg=blue>Installing corpus</>: {name}")
                dl.download(name, quiet=True)
            else:
                if dl.is_stale(name):
                    if not dgloss.quiet:
                        self._print(f"<fg=blue>Updating corpus</>: {name}")
                    dl.update(quiet=True)
        self.lemmatizer = stem.WordNetLemmatizer()

    # TODO: Instead of scanning the whole directory tree to build up the
    # config, do it incrementally (i.e., adding a `.dgloss.conf` to a specific
    # subdirectory should only apply those rules to the contents of that
    # directory)
    def _scan_dir(self):
        dirname = self.config_dirname
        if not dgloss.quiet:
            self._print(
                f"<fg=blue>Scanning configuration directory</>: {dirname}"
            )
        for root, dirs, files in os.walk(dirname):
            # Sort directories and files so that we process them in a
            # order (alphabetical, ascending)
            dirs.sort()
            files.sort()
            for filename in files:
                if filename == ".dgloss.conf":
                    filename = os.path.join(root, filename)
                    self._process_file(filename)

    def _process_file(self, filename):
        if dgloss.verbose:
            self._print(f"<fg=blue>Reading configuration file</>: {filename}")
        text = charset.decode_file(filename)
        text_lines = text.splitlines()
        instructions = []
        table_lines = []
        for line_num, line in enumerate(text_lines):
            line_num += 1
            instruction = self._process_line(filename, line_num, line)
            if not instruction:
                continue
            instructions.append(instruction)
            argument_type = instruction.argument.__class__.__name__
            table_line = [
                instruction.line_num,
                instruction.command_name,
                instruction.option_name,
                argument_type,
            ]
            table_lines.append(table_line)
        if self._parse_errors:
            raise dgloss.ParseError(self._parse_errors)
        if dgloss.verbose:
            self._print(f"<fg=green>Configuration for</>: {filename}\n")
            headers = ["Line", "Command", "Option", "Argument"]
            table = tabulate(
                table_lines, headers=headers, tablefmt=dgloss.table_format
            )
            self._print(table)
            print("")
        # TODO: Make a private variable
        self.instructions = instructions

    def _process_line(self, filename, line_num, line):
        line = line.strip()
        if not line:
            # Ignore empty lines
            return
        if line.startswith("#"):
            # Ignore comments
            return
        instruction = Instruction(filename, line_num)
        try:
            command_name, option_name, argument = line.split(" ")
        except ValueError:
            tokens_num = len(line.split(" "))
            tokens_num_word = inflect.engine().number_to_words(tokens_num)
            tokens_num_word = tokens_num_word.replace("-", " ")
            msg = f"Expected three tokens (got {tokens_num_word})"
            parse_error = [filename, line_num, msg]
            self._parse_errors.append(parse_error)
            return
        instruction.command_name = command_name.lower().strip()
        instruction.option_name = option_name.lower().strip()
        instruction.argument = argument.strip()
        self._handle_instruction(instruction)
        return instruction

    def _handle_instruction(self, instruction):
        if instruction.command_name == "use":
            return self._run_command_use(instruction)
        if instruction.command_name == "ignore":
            return self._run_command_ignore(instruction)
        msg = f"Invalid command: {instruction.command_name}"
        parse_error = [instruction.filename, instruction.line_num, msg]
        self._parse_errors.append(parse_error)
        return instruction

    def _run_command_use(self, instruction):
        if instruction.option_name == "corpus":
            return self._run_command_use_corpus(instruction)
        msg = f"Invalid option: {instruction.option}"
        parse_error = [instruction.filename, instruction.line_num, msg]
        self._parse_errors.append(parse_error)
        return instruction

    def _run_command_use_corpus(self, instruction):
        for corpus_def in self.PKG_WORD_FREQ_CORPORA:
            if corpus_def["name"] == instruction.argument:
                self.word_freq_corpus = corpus_def
                break
        if self.word_freq_corpus:
            abs_filename = dgloss.data_path.joinpath(
                self.word_freq_corpus["data_filename"]
            )
            self.word_freq_corpus["abs_filename"] = abs_filename
            return instruction
        msg = f"Invalid argument: {instruction.argument}"
        parse_error = [instruction.filename, instruction.line_num, msg]
        self._parse_errors.append(parse_error)

    def _run_command_ignore(self, instruction):
        if instruction.option_name == "case":
            return self._run_command_ignore_case(instruction)
        if instruction.option_name == "stopwords":
            return self._run_command_ignore_stopwords(instruction)
        if instruction.option_name == "literal":
            return self._run_command_ignore_literal(instruction)
        if instruction.option_name == "regex":
            return self._run_command_ignore_regex(instruction)
        # TODO: Implement debug mode
        msg = f"Invalid option: {instruction.option}"
        parse_error = [instruction.filename, instruction.line_num, msg]
        self._parse_errors.append(parse_error)
        return

    def _run_command_ignore_case(self, instruction):
        if instruction.argument not in ["true", "false"]:
            # TODO: Implement debug mode
            msg = f"Invalid argument: {instruction.argument}"
            parse_error = [instruction.filename, instruction.line_num, msg]
            self._parse_errors.append(parse_error)
            return
        argument = inflection.titleize(instruction.argument)
        self.ignore_case = ast.literal_eval(argument)
        instruction.argument = self.ignore_case
        return instruction

    def _run_command_ignore_stopwords(self, instruction):
        # TODO: convert this to a set of regexps
        # re_obj = re.compile(re.escape(str))
        try:
            # Attempt to load the stopwords for language indicated by the value
            # of `argument` (e.g., "english")
            stopwords_set = set(stopwords.words(instruction.argument))
        except OSError:
            # TODO: Implement debug mode
            msg = f"Invalid argument: {instruction.argument}"
            parse_error = [instruction.filename, instruction.line_num, msg]
            self._parse_errors.append(parse_error)
            return
        self.ignore_literals.update(stopwords_set)
        instruction.argument = stopwords_set
        return instruction

    def _run_command_ignore_literal(self, instruction):
        self.ignore_literals.add(instruction.argument)
        return instruction

    def _run_command_ignore_regex(self, instruction):
        try:
            re_obj = re.compile(instruction.argument)
        except re.error:
            # TODO: Implement debug mode
            msg = f"Invalid argument: {instruction.argument}"
            parse_error = [instruction.filename, instruction.line_num, msg]
            self._parse_errors.append(parse_error)
            return
        self.ignore_regexes.add(re_obj)
        instruction.argument = re_obj
        return instruction
