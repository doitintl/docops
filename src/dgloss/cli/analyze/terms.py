"""Find terms that may be candidates for inclusion in a glossary

Usage:

  {entry_point} [options] <DIR>
  {entry_point} [options] (-h | --help)
  {entry_point} [options] (--version)
  {entry_point} [options] (--show-formats)
  {entry_point} [options] (--print-cache)
  {entry_point} [options] (--delete-cache)

This program will:

  - Scan the given directory (`<DIR>`) for files (ignoring any directory or
    filename that begins with the `.` character).

  - Tokenize all files (that can be decoded as character data) into a list of
    unique terms, regardless of file format.

  - Attempt to group terms using lemmatization (i.e., convert inflected words
    to their standard to dictionary form).

  - Count how often every term is used and compare this with word frequency
    data from a standard (i.e., non-technical) English-language corpus.

  - Print a list of terms that appear more often than expected, ranked on a
    logarithmic scale, and sorted from highest to lowest frequency.

Options:

  -h, --help         Print this help message and exit

  --version          Print the software version number and exit

  -v, --verbose      Display verbose output messages

  -q, --quiet        Silence most output messages

  --disable-ansi     Disable ANSI escape code formatting

  -l, --limit=NUM    Limit the number of result rows [default: 100]

  -f, --format=NAME  Specify the table format [default: simple]

  --show-formats     Print a list of supported table formats and exit

  --print-cache      Print the location of the cache directory and exit

  --delete-cache     Delete the cache directory and exit

  --show-warnings    Show Python warnings
"""

import sys
import warnings

from docopt import docopt

import tabulate

import dgloss
from dgloss import color
from dgloss.analyzers.terms import TermAnalyzer
from dgloss.config import Configuration

__entry_point__ = None

for entry_point in dgloss.__dist__.entry_points:
    if entry_point.module == __name__:
        __entry_point__ = entry_point.name

_doc = __doc__.format(entry_point=__entry_point__)


class TermsCommand:

    # Allowed options
    help = None
    version = None
    verbose = None
    quiet = None
    disable_ansi = None
    limit = None
    format = None
    show_formats = None
    print_cache = None
    delete_cache = None
    show_warnings = None

    # Allowed positional arguments
    dir = None

    # Configuration settings
    # TODO: Set these values using a configuration file (they are hardcoded for
    # the time being)
    ignore_case = True
    ignore_stop_words = True

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
        self.set_pkg_options()

    def set_class_attr(self, name, value):
        # Raise an exception if the attribute is not a predefined class
        # attribute
        getattr(self, name)
        # Set the value of the predefined class attribute
        setattr(self, name, value)

    # TODO: I think this is probably an anti-pattern and these should be passed
    # through in other ways
    def set_pkg_options(self):
        dgloss.verbose = self.verbose
        dgloss.quiet = self.quiet
        dgloss.disable_ansi = self.disable_ansi

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
        return self.do_print_table()

    def exit_help(self):
        print(_doc.strip())
        return 0

    def do_delete_cache(self):
        config = Configuration()
        config.delete_cache()
        return 0

    def do_print_cache(self):
        config = Configuration()
        if not config.print_cache_path():
            return 1
        return 0

    def do_show_formats(self):
        formatter = color.Formatter()
        msg = "Supported table formats:\n\n"
        for format in tabulate.tabulate_formats:
            msg += f" - {format}\n"
        formatter.print(msg.strip())
        return 0

    def do_print_table(self):
        analyzer = TermAnalyzer()
        if self.ignore_case:
            analyzer.ignore_case()
        if self.ignore_stop_words:
            analyzer.ignore_stop_words()
        analyzer.init_nltk()
        analyzer.use_pkg_corpus("leeds")
        analyzer.scan_dir(self.dir)
        analyzer.print_ranks(self.limit, self.format)
        return 0


def run():
    # TODO: Switch to the new version of docopt? Annoyed with this one...
    # TODO: Switch to using colors for the help output
    doc = _doc.replace("Usage:\n", "Usage:")
    args = docopt(doc, help=False, version=dgloss.__version__)
    # Default to exiting with an error unless the `run` method indicates a
    # successful operation
    exit_code = 1
    try:
        command = TermsCommand(args)
        exit_code = command.run()
    except KeyboardInterrupt:
        # Exit silently when the the user terminates the program early
        pass
    except BrokenPipeError:
        # Exit silently when the pipe is broken (e.g., when piped to a program
        # like `head`)
        pass
    sys.exit(exit_code)
