"""Find terms that may be candidates for inclusion in a glossary

Usage:

  {cmd_name} [options] <DIR>
  {cmd_name} [options] (-h | --help)
  {cmd_name} [options] (--version)
  {cmd_name} [options] (--show-formats)
  {cmd_name} [options] (--print-cache)
  {cmd_name} [options] (--delete-cache)

  {row_limit}

This program will:

  - Scan the target directory (`<DIR>`) for files (ignoring any directory or
    filename that begins with the `.` character).

  - Tokenize all files (that can be decoded as character data) into a list of
    unique terms, regardless of file format.

  - Attempt to group terms using lemmatization (i.e., convert inflected words
    to their standard to dictionary form).

  - Count how often every term is used and compare this with word frequency
    data from a standard (i.e., non-technical) English-language corpus.

  - Print a list of terms that appear more often than expected, ranked on a
    logarithmic scale, and sorted from highest to lowest frequency.

Basic options:

  -h, --help               Print this help message and exit

  --version                Print the software version number and exit

  -v, --verbose            Display verbose output messages

  -q, --quiet              Silence most output messages

  --disable-ansi           Disable ANSI escape code formatting

  -c --config-dir=DIR      Search `DIR` for `.dgloss.conf` files instead of the
                           target directory

  -l, --row-limit=NUM      Limit results to `NUM` rows [default: {row_limit}]

  -r, --table-format=TYPE  Use table format `TYPE` [default: {table_format}]

  --show-formats           Print a list of supported table formats and exit

  --print-cache            Print the location of the cache directory and exit

  --delete-cache           Delete the cache directory and exit

  --show-warnings          Show Python warnings
"""

import sys
import warnings
import pathlib

import editorconfig
from editorconfig.handler import EditorConfigHandler

import docopt

import tabulate

import dgloss
from dgloss.print import Printer
from dgloss.config import Configuration
from dgloss.analyzers.terms import TermAnalyzer
from dgloss.cache import Cache

# Format the docstring
cmd_path = pathlib.PurePath(sys.argv[0])
format_dict = {
    "cmd_name": cmd_path.name,
    "row_limit": dgloss.row_limit,
    "table_format": dgloss.table_format,
}
# Not needed for now, but may need again the future
#
# Unwrap lines marked up with `<unwrap>`, which is used to wrap the docstring
# to fit the 79 char limit for source files
# __doc__ = re.sub("\n *<unwrap>", " ", __doc__)
__doc__ = __doc__.format(**format_dict)


class TermsCommand:

    # Allowed options
    help = None
    version = None
    verbose = None
    quiet = None
    disable_ansi = None
    config_dir = None
    row_limit = None
    table_format = None
    show_formats = None
    print_cache = None
    delete_cache = None
    show_warnings = None

    # Allowed positional arguments
    dir = None

    _config = None
    _cache = None
    _analyzer = None

    def __init__(self, args):
        # Process the dict returned by docopt and use it to automatically set
        # the predefined class attributes
        for key, value in args.items():
            if key.startswith("--"):
                attr_name = key.lstrip("--").replace("-", "_")
                self.set_class_attr(attr_name, value)
                continue
            if key.startswith("<"):
                attr_name = key.lstrip("<").rstrip(">").lower()
                self.set_class_attr(attr_name, value)
                continue
            attr_name = key.lower()
            self.set_class_attr(attr_name, value)
        self._config = Configuration(self.dir, self.config_dir)
        self._cache = Cache()
        self._validate_docstring()
        self.set_pkg_options()

    def _validate_docstring(self):
        try:

            parser = EditorConfigHandler(__file__, dgloss.editorconfig_path)
            config = parser.get_configurations()
        except editorconfig.EditorConfigError:
            raise dgloss.ProgramError(
                "Unable to parse package `.editorconfig` file"
            )
        try:
            max_line_length = int(config["max_line_length"])
        except KeyError:
            raise dgloss.ProgramError(
                "No `max_line_length` set in package `.editorconfig` file"
            )
        for line_num, line in enumerate(__doc__.splitlines()):
            if len(line) > max_line_length:
                raise dgloss.ProgramError(
                    f"Docstring line {line_num} "
                    + f"exceeds max line length ({max_line_length})"
                )

    def set_class_attr(self, name, value):
        # Raise an exception if the attribute is not a predefined class
        # attribute
        getattr(self, name)
        # Set the value of the predefined class attribute
        setattr(self, name, value)

    # TODO: I think this is probably an anti-pattern and these should be passed
    # through in other ways
    def set_pkg_options(self):
        # Set module options
        dgloss.verbose = self.verbose
        dgloss.quiet = self.quiet
        dgloss.disable_ansi = self.disable_ansi
        dgloss.table_format = self.table_format
        dgloss.row_limit = self.row_limit

    def run(self):
        if self.help:
            return self.do_help()
        if not self.show_warnings:
            warnings.filterwarnings("ignore")
        if self.delete_cache:
            return self.do_delete_cache()
        if self.print_cache:
            return self.do_print_cache()
        if self.show_formats:
            return self.do_show_formats()
        self.do_main()

    def do_help(self):
        print(__doc__.strip())
        return 0

    def do_delete_cache(self):
        self._cache.delete_cache()
        return 0

    def do_print_cache(self):
        if not self._cache.print_cache_path():
            return 1
        return 0

    def do_show_formats(self):
        printer = Printer()
        msg = "Supported table formats:\n\n"
        for format in tabulate.tabulate_formats:
            msg += f" - {format}\n"
        printer.print(msg.strip())
        return 0

    def do_main(self):
        self._config.load()
        self._analyzer = TermAnalyzer(self._config)
        self._analyzer.run()
        self._analyzer.print_ranks()
        return 0


def run():
    # TODO: Switch to the new version of docopt? Annoyed with this one...
    # TODO: Switch to using colors for the help output
    printer = Printer()
    # Default to exiting with an error unless the `run` method indicates a
    # successful operation
    exit_code = 1
    try:
        try:
            # TODO: There's gotta be a way of doing this differently
            doc = __doc__.replace("Usage:\n", "Usage:")
            args = docopt.docopt(doc, help=False, version=dgloss.__version__)
        except docopt.DocoptExit as err:
            raise dgloss.CliError(err)
        command = TermsCommand(args)
        exit_code = command.run()
    except KeyboardInterrupt:
        # Exit silently when the the user terminates the program early
        pass
    except BrokenPipeError:
        # Exit silently when the pipe is broken (e.g., when piped to a program
        # like `head`)
        pass
    except dgloss.Error as err:
        printer.print(str(err), sys.stderr)
    sys.exit(exit_code)
