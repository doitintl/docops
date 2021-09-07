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


def do_help():
    print(_doc.strip())


def do_set_pkg_options(verbose, quiet, disable_ansi):
    dgloss.verbose = verbose
    dgloss.quiet = quiet
    dgloss.disable_ansi = disable_ansi


def do_delete_cache():
    config = Configuration()
    config.delete_cache()


def do_print_cache():
    config = Configuration()
    if not config.print_cache_path():
        sys.exit(1)


def do_show_formats():
    formatter = color.Formatter()
    msg = "Supported table formats:\n\n"
    for format in tabulate.tabulate_formats:
        msg += f" - {format}\n"
    formatter.print(msg.strip())


def do_process_dir(dir, limit, format):
    analyzer = TermAnalyzer()
    analyzer.use_pkg_corpus("leeds")
    analyzer.init_nltk()
    analyzer.scan_dir(dir)
    analyzer.print_ranks(limit, format)


def main(args):
    if args["--help"]:
        do_help()
        return
    do_set_pkg_options(
        args["--verbose"], args["--quiet"], args["--disable-ansi"]
    )
    if not args["--show-warnings"]:
        warnings.filterwarnings("ignore")
    if args["--delete-cache"]:
        do_delete_cache()
        return
    if args["--print-cache"]:
        do_print_cache()
        return
    if args["--show-formats"]:
        do_show_formats()
        return
    do_process_dir(args["<DIR>"], args["--limit"], args["--format"])


def run():
    # TODO: Switch to the new version of docopt? Annoyed with this one...
    # TODO: Switch to using colors for the help output
    doc = _doc.replace("Usage:\n", "Usage:")
    args = docopt(doc, help=False, version=dgloss.__version__)
    try:
        main(args)
    except KeyboardInterrupt:
        # Exit silently when the the user terminates the program early
        pass
    except BrokenPipeError:
        # Exit silently when the pipe is broken (e.g., when piped to a program
        # like `head`)
        pass
    sys.exit(0)
