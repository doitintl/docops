# MIT License
# Copyright 2021, DoiT International
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import ast
import os
import pathlib
import yaml
import inspect

from collections import UserDict
from collections import defaultdict

import inflect
import inflection
import nltk
from doitintl import docops
from doitintl.docops.gloss import charset
from doitintl.docops.gloss.cache import Cache
from doitintl.docops.gloss.print import Printer
from nltk import downloader
from nltk import stem

# Stopword libraries
from nltk import corpus as nltk_corpus
import stopwordsiso
import spacy


from tabulate import tabulate

# TODO: For debugging purposes only
import sys
from pprint import pprint

# TODO: Change to Command?
class Instruction:

    _command_name = None
    _option_name = None
    _argument = None

    _command = None
    _option = None


class ConfigurationParser:

    # This is the closest to a schema we're going to get for now (while code
    # changes settle down)
    _DEFAULTS = {
        "corpora": {"word-frequency": "leeds"},
        "wordlists": {"stopwords": ["english"], "builtins": [], "custom": []},
        "words": {},
        "regexes": {
            # This regular expression matches any string with no alphanumeric
            # characters
            "ngram-seperators": r"^[^\d\w]+$",
        },
        "lemmas": {
            "case-sensitive": False,
            "ignore": {
                "wordlists": [],
                "words": [],
                "regexes": [],
            },
        },
        "ngrams": {
            "case-sensitive": False,
            "seperators": {
                "wordlists": ["nltk-en", "iso-en", "custom"],
                "words": [],
                "regexes": [],
            },
            "ignore": {
                "wordlists": [],
                "words": [],
                "regexes": [],
            },
            "trim": {
                "wordlists": [stopwords],
                "words": [],
                "regexes": [],
            },
        },
    }

    # TODO: Add more corpora to test with
    _CORPORA = {
        "word-frequency": [
            {
                "name": "leeds",
                "data_filename": "corpora/leeds.txt.gz",
                "re": r"(?P<rank>\d+) +(?P<ipm>\d+(\.?\d+)) +(?P<lemma>\w+)",
            }
        ]
    }

    _literals_dict = {}
    _regexes_dict = {}

    _config = None

    def update(self, config_obj, yaml):
        self._config = config_obj
        self._print = self._config._print
        if docops._get_max_verbose():
            self._print("<success>Parsed YAML:</success>\n")
            pprint(yaml)
            print()
        self._corpora(yaml)
        self._wordlists(yaml)
        self._config.preview()
        self._words(yaml)
        self._regexes(yaml)
        self._lemmas(yaml)
        self._ngrams(yaml)
        self._terms(yaml)

    # Utility methods
    # -------------------------------------------------------------------------

    def _force_bool(self, input):
        # Force an arbitary value into boolean
        if input is not True:
            return False
        return True

    def _update_regexes_set(
        self, desc, target_set, regexes_ittr, literal=False
    ):
        # Convert each stopword into a regexp
        for regex_string in regexes_ittr:
            regex = regex_string
            if literal:
                # Make sure thst literals can't be interpreted as reglular
                # expressions
                regex_string = re.escape(regex_string)
                # Convert literals into regexes that have to match the whole
                # string
                regex = f"^{regex_string}$"
            try:
                re_obj = re.compile(regex)
            except re.error as err:
                if literal:
                    err_msg = (
                        f"Could not parse literal as regex: {regex_string}"
                    )
                else:
                    err_msg = f"Could not parse regex: {regex_string}"
                raise docops.ConfigurationError(err_msg) from err
            target_set.add(re_obj)
            if docops._get_max_verbose():
                self._print(f"<success>Added {desc}:</success> ", regex_string)

    # Top-level `corpus` key
    # -------------------------------------------------------------------------

    def _corpora(self, yaml):
        yaml = yaml.get("corpus", {})
        self._corpora_word_frequency(yaml)

    def _corpora_word_frequency(self, yaml):
        default = self._DEFAULTS["corpora"]["word-frequency"]
        corpus_name = yaml.get("word-frequency", default)
        if not corpus_name:
            raise docops.ConfigurationError("No word frequency corpus set")
        if docops._get_max_verbose():
            self._print(
                "<success>Set word frequency corpus:</success>: ", corpus_name
            )
        corpus = None
        for corpus_def in self._CORPORA["word-frequency"]:
            if corpus_def["name"] == corpus_name:
                corpus = corpus_def
                abs_filename = docops._get_data_path().joinpath(
                    corpus["data_filename"]
                )
                corpus["abs_filename"] = abs_filename
        if not corpus:
            raise docops.ConfigurationError(
                f"Reference corpus not found: {corpus_name}"
            )
        self._config._corpus_word_frequency = corpus

    # Top-level `wordlists` key
    # -------------------------------------------------------------------------

    def _wordlists(self, yaml):
        yaml = yaml.get("wordlists", {})
        self._wordlists_stopwords(yaml)
        self._wordlists_builtins(yaml)
        self._wordlists_custom(yaml)

    def _wordlists_stopwords(self, yaml):
        default_languages = self._DEFAULTS["wordlists"]["stopwords"]
        languages = yaml.get("stopwords", default_languages)

        iso_stopwords = stopwordsiso.stopwords("en")

        nltk_stopwords = nltk_corpus.stopwords.words("english")

        # for this next bit, it needs to be added as a package dependency using
        # a URL and the latest release version
        # latest: https://spacy.io/models/en
        # https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.1.0/en_core_web_sm-3.1.0.tar.gz#egg=en_core_web_sm
        en_model = spacy.load("en_core_web_sm")

        spacy_stopwords = en_model.Defaults.stop_words

        for language in languages:
            try:
                language_stopwords = set(stopwords.words(language))
            except OSError as err:
                raise docops.ConfigurationError(
                    f"No stopwords found for language: {language}"
                ) from err
            if docops._get_more_verbose():
                self._print(
                    "<success>Adding stopwords for:</success>", language
                )
            self._update_regexes_set(
                "stopword",
                self._config._wordlists["stopwords"],
                language_stopwords,
                literal=True,
            )

    def _wordlists_builtins(self, yaml):
        pass

    def _wordlists_builtins_name(self, yaml):
        pass

    def _wordlists_custom(self, yaml):
        # RESCUED CODE FROM OLD FUNCTION CLOSEST TO THIS ONE
        # stopwords = yaml.get("custom", [])
        # self._update_regexes_set(
        #     "custom stopword", self._config._stopwords_set, stopwords
        # )
        # if docops._get_more_verbose():
        #     self._print("<success>Adding custom stopwords</success>")
        pass

    def _wordlists_custom_file(self, yaml):

        pass

    # Top-level `words` key
    # -------------------------------------------------------------------------

    def _words(self, yaml):
        literals = yaml.get("literals", [])
        for name, literals_list in literals:
            named_literals_set = set()
            try:
                named_literals_set = self._literals_dict[name]
            except KeyError:
                self._literals_dict[name] = named_literals_set
            literals_set = set(literals_list)
            self._update_regexes_set(
                "literal", named_literals_set, literals_set, literal=True
            )
            if docops._get_more_verbose():
                self._print("<success>Adding literals:</success>", name)

    # Top-level `regexes` key
    # -------------------------------------------------------------------------

    # TODO: DRY this out. it's the same code as `_literals`
    def _regexes(self, yaml):
        regexes = yaml.get("regexes", [])
        for name, regexes_list in regexes.items():
            named_regexes_set = set()
            try:
                named_regexes_set = self._regexes_dict[name]
            except KeyError:
                self._regexes_dict[name] = named_regexes_set
            regexes_set = set(regexes_list)
            self._update_regexes_set("regex", named_regexes_set, regexes_set)
            if docops._get_more_verbose():
                self._print("<success>Adding regexes:</success> ", name)

    # Top-level `lemmas` key
    # -------------------------------------------------------------------------

    def _lemmas(self, yaml):
        yaml = yaml.get("lemmas", {})
        self._lemmas_case_sensitive(yaml)
        self._lemmas_ignore(yaml)

    def _lemmas_case_sensitive(self, yaml):
        default = self._DEFAULTS["lemmas"]["case-sensitive"]
        case_sensitive = yaml.get("case-sensitive", default)
        case_sensitive = self._force_bool(case_sensitive)
        if docops._get_more_verbose():
            adverb = not case_sensitive and "not"
            self._print(
                f"<info>Lemmas will {adverb}"
                + "be converted to lower case</info>"
            )
        self._config._lemmas_case_sensitive = case_sensitive

    def _lemmas_ignore(self, yaml):
        yaml = yaml.get("ignore", {})
        self._lemmas_case_sensitive(yaml)
        self._lemmas_ignore_stopwords(yaml)
        self._lemmas_ignore_literals(yaml)
        self._lemmas_ignore_regexes(yaml)

    def _lemmas_ignore_wordlists(self, yaml):
        # RESCUED OLD CODE
        # ignore_stopwords = yaml.get("stopwords", True)
        # ignore_stopwords = self._force_bool(ignore_stopwords)
        # if docops._get_more_verbose():
        #     adverb = not ignore_stopwords and "not"
        #     self._print(f"<info>Lemmas stopwords {adverb} be ignored</info>")
        # stopwords_set = self._config._stopwords_set
        # if ignore_stopwords:
        #     self._config._lemmas_ignore_set.update(stopwords_set)
        pass

    def _lemmas_ignore_word(self, yaml):
        # RESCUED CODE
        # literals_set_list = yaml.get("literals", [])
        # for literals_set_name in literals_set_list:
        #     if docops._get_more_verbose():
        #         self._print(
        #             "<info>Lemmas will ignore literals:</info> ",
        #             literals_set_name,
        #         )
        #     literals_set = self._literals_dict[literals_set_name]
        #     self._config._lemmas_ignore_set.update(literals_set)
        pass

    def _lemmas_ignore_regexes(self, yaml):
        regexes_set_list = yaml.get("regexes", [])
        for regexes_set_name in regexes_set_list:
            if docops._get_more_verbose():
                self._print(
                    "<info>Lemmas will ignore regexes:<info> ",
                    regexes_set_name,
                )
            regexes_set = self._regexes_dict[regexes_set_name]
            self._config._lemmas_ignore_set.update(regexes_set)

    # Top-level `ngrams` key
    # -------------------------------------------------------------------------

    # TODO: DRY OUT THIS CODE WITH SECTION ABOVE

    def _ngrams(self, yaml):
        yaml = yaml.get("ngrams", {})
        self._ngrams_case_sensitive(yaml)
        self._ngrams_ignore(yaml)

    def _ngrams_case_sensitive(self, yaml):
        default = self._DEFAULTS["ngrams"]["case-sensitive"]
        case_sensitive = yaml.get("case-sensitive", default)
        case_sensitive = self._force_bool(case_sensitive)
        if docops._get_more_verbose():
            adverb = not case_sensitive and "not"
            self._print(
                f"<info>ngrams will {adverb}"
                + "be converted to lower case</info>"
            )
        self._config._ngrams_case_sensitive = case_sensitive

    def _ngrams_seperators(self, yaml):
        pass

    def _ngrams_seperators_wordlists(self, yaml):
        pass

    def _ngrams_seperators_words(self, yaml):
        pass

    def _ngrams_seperators_regexes(self, yaml):
        pass

    def _ngrams_ignore(self, yaml):
        yaml = yaml.get("ignore", {})
        self._ngrams_ignore_wordlists(yaml)
        self._ngrams_ignore_words(yaml)
        self._ngrams_ignore_regexes(yaml)

    def _ngrams_ignore_wordlists(self, yaml):
        # RESCUED CODE
        # ignore_stopwords = yaml.get("stopwords", True)
        # ignore_stopwords = self._force_bool(ignore_stopwords)
        # if docops._get_more_verbose():
        #     adverb = not ignore_stopwords and "not"
        #     self._print(f"<info>ngrams stopwords {adverb} be ignored</info>")
        # stopwords_set = self._config._stopwords_set
        # if ignore_stopwords:
        #     self._config._ngrams_ignore_set.update(stopwords_set)
        pass

    def _ngrams_ignore_words(self, yaml):
        literals_set_list = yaml.get("literals", [])
        for literals_set_name in literals_set_list:
            if docops._get_more_verbose():
                self._print(
                    "<info>ngrams will ignore literals:</info> ",
                    literals_set_name,
                )
            literals_set = self._literals_dict[literals_set_name]
            self._config._ngrams_ignore_set.update(literals_set)

    def _ngrams_ignore_regexes(self, yaml):
        regexes_set_list = yaml.get("regexes", [])
        for regexes_set_name in regexes_set_list:
            if docops._get_more_verbose():
                self._print(
                    "<info>ngrams will ignore regexes:<info> ",
                    regexes_set_name,
                )
            regexes_set = self._regexes_dict[regexes_set_name]
            self._config._ngrams_ignore_set.update(regexes_set)

    def _terms(self, yaml):
        pass


# TODO: Should probably split this off into a seperate file


class Configuration(UserDict):

    _CONFIG_FILENAMES = [
        ".dgloss.yaml",
        ".dgloss.yml",
        "dgloss.yaml",
        "dgloss.yml",
    ]

    # TODO: Additional stop word lirbraries with more words:
    # https://medium.com/@saitejaponugoti/stop-words-in-nlp-5b248dadad47

    # https://github.com/anvaka/common-words

    # See https://www.nltk.org/nltk_data/
    _NLTK_CORPORA = ["punkt", "wordnet", "stopwords"]

    _target_dirname = None
    _config_dirname = None

    _printer = None
    _cache = None
    _lemmatizer = None

    _corpus_word_frequency = None

    _wordlists = {"stopwords": set(), "builtins": set()}

    _lemmas_case_sensitive = None
    _lemmas_ignore_set = set()

    _ngrams_case_sensitive = None
    _ngarms_seperators_set = set()
    _ngarms_ignore_set = set()
    _ngarms_trim_set = set()

    _terms = {}

    _terms_ngrams = {}

    def __init__(self):
        self._printer = Printer()
        self._cache = Cache()

    def _print(self, *args):
        self._printer.print(*args)

    def load(self, target_dirname, config_dirname):
        self._target_dirname = pathlib.Path(target_dirname)
        self._config_dirname = pathlib.Path(target_dirname)
        # If the user invoked the program that didn't require `DIR` to be set,
        # this value will be None
        if config_dirname:
            self._config_dirname = pathlib.Path(config_dirname)
        self._init_nltk()
        self._scan_dir()

    def _init_nltk(self):
        if docops._get_more_verbose():
            self._print("<info>Initializing the NLTK library<info>")
        cache_path = self._cache.get_cache_path()
        nltk_dir = cache_path.joinpath("nltk")
        nltk_dir.mkdir(parents=True, exist_ok=True)
        nltk.data.path.insert(0, nltk_dir)
        dl = downloader.Downloader()
        for name in self._NLTK_CORPORA:
            if not dl.is_installed(name):
                if not docops._get_quiet():
                    self._print("<infoInstalling corpus</info>: ", name)
                dl.download(name, quiet=True)
            else:
                if dl.is_stale(name):
                    if not docops._get_quiet():
                        self._print("<info>Updating corpus</info>: ", name)
                    dl.update(quiet=True)
        self._lemmatizer = stem.WordNetLemmatizer()

    def get_lemmatizer(self):
        return self._lemmatizer

    def get_target_dirname(self):
        return self._target_dirname

    def get_config_dirname(self):
        return self._config_dirname

    # TODO:
    #
    # Maybe, instead of scanning the whole directory tree to build up the
    # config, do it incrementally (i.e., adding a config file to a specific
    # subdirectory should only apply those rules to the contents of that
    # directory)

    def _scan_dir(self):
        dirname = self._config_dirname
        if docops._get_verbose():
            self._print(
                "<info>Scanning configuration directory:</info> ", dirname
            )
        for root, dirs, files in os.walk(dirname):
            # Sort directories and files so that we process them in a
            # order (alphabetical, ascending)
            dirs.sort()
            files.sort()
            for filename in files:
                if filename in self._CONFIG_FILENAMES:
                    filename = os.path.join(root, filename)
                    self._process_file(filename)

    def _process_file(self, filename):
        if not docops._get_quiet():
            self._print("<fg=blue>Reading configuration file</>: ", filename)
        text = charset.decode_file(filename)
        yaml_config = yaml.safe_load(text)
        config_parser = ConfigurationParser()
        config_parser.update(self, yaml_config)

    def preview(self):
        print("==============================================================")
        print("Results")
        print("==============================================================")
        print()
        print("_corpus_word_frequency")
        print("--------------------------------------------------------------")
        print()
        pprint(self._corpus_word_frequency)
        print()
        print("_wordlists")
        print("--------------------------------------------------------------")
        print()
        pprint(self._wordlists)
        print()
        print("_lemmas_case_sensitive")
        print("--------------------------------------------------------------")
        print()
        pprint(self._lemmas_case_sensitive)
        print()
        print("_lemmas_ignore_set")
        print("--------------------------------------------------------------")
        print()
        pprint(self._lemmas_ignore_set)
        print()
        print("_ngrams_case_sensitive")
        print("--------------------------------------------------------------")
        print()
        pprint(self._ngrams_case_sensitive)
        print()
        print("_ngarms_seperators_set")
        print("--------------------------------------------------------------")
        print()
        pprint(self._ngarms_seperators_set)
        print()
        print("_ngarms_ignore_set")
        print("--------------------------------------------------------------")
        print()
        pprint(self._ngarms_ignore_set)
        print()
        print("_ngarms_trim_set")
        print("--------------------------------------------------------------")
        print()
        pprint(self._ngarms_trim_set)
        print()
        print("_terms")
        print("--------------------------------------------------------------")
        print()
        pprint(self._terms)
        print()
        print("_terms_ngrams")
        print("--------------------------------------------------------------")
        print()
        pprint(self._terms_ngrams)
        print()
        sys.exit(0)
