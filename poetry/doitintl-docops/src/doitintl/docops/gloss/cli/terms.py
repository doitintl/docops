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


# TODO: Colorize this output
"""
Find terms that may be candidates for inclusion in a glossary

Usage:

  {cmd_name} [options] <DIR>
  {cmd_name} [options] (-h | --help)
  {cmd_name} [options] (--version)
  {cmd_name} [options] (--show-output-types)
  {cmd_name} [options] (--show-table-formats)
  {cmd_name} [options] (--print-cache)
  {cmd_name} [options] (--delete-cache)

This program will:

  - Scan the target directory (`<DIR>`) for configuration files named
    `.gloss.conf` and process them prior to analysis.

    You can use the `--config-dir` option to specify an alternative directory
    to scan for configuration files.

  - Scan the target directory (`<DIR>`) for files (ignoring any directory or
    filename that begins with the `.` character).

  - Tokenize all files (that can be decoded as character data) into a list of
    unique terms, regardless of file format.

  - Attempt to group terms using lemmatization (i.e., convert inflected words
    to their standard to dictionary form).

  - Count how often every term is used and compare this with word frequency
    data from a standard (i.e., non-technical) English-language corpus.

  - Print a list of terms that appear more often than expected, ranked on a
    logarithmic scale, and sorted from the highest to the lowest frequency.

Basic options:

  -h, --help               Print this help message and exit

  --version                Print the software version number and exit

  -v, --verbose            Display verbose output messages

  -q, --quiet              Silence most output messages

  --disable-ansi           Disable ANSI escape code formatting

  -c --config-dir=DIR      Search `DIR` for `.gloss.conf` files instead of the
                           target directory

  -l, --term-limit=NUM     Limit results to `NUM` terms [default: {term_limit}]

  -o, --output-type=TYPE   Use output TYPE [default: table]

  --show-output-types      Print a list of supported output types and exit

  -t, --table-format=TYPE  Use table format `TYPE` [default: {table_format}]

  --show-table-formats     Print a list of supported table formats and exit

  --print-cache            Print the location of the cache directory and exit

  --delete-cache           Delete the cache directory and exit

  --show-warnings          Show Python warnings
"""

import sys
import warnings
import pathlib

import configparser

import docopt

import tabulate

from doitintl import docops
from doitintl.docops.gloss.print import Printer
from doitintl.docops.gloss.config import Configuration
from doitintl.docops.gloss.analyzers.terms import TermAnalyzer
from doitintl.docops.gloss.cache import Cache

# Format the docstring
cmd_path = pathlib.PurePath(sys.argv[0])
cmd_name = cmd_path.name
format_dict = {
    "cmd_name": cmd_name,
    "term_limit": docops.term_limit,
    "table_format": docops.table_format,
}
# Not needed for now, but may need again the future
#
# Unwrap lines marked up with `<unwrap>`, which is used to wrap the docstring
# to fit the 79 char limit for source files
# __doc__ = re.sub("\n *<unwrap>", " ", __doc__)
__doc__ = __doc__.format(**format_dict)


class TermsCommand:

    OUTPUT_TYPES = ["none", "table"]
    TABLE_FORMATS = tabulate.tabulate_formats

    # Allowed options
    help = None
    version = None
    verbose = None
    quiet = None
    disable_ansi = None
    config_dir = None
    output_type = None
    show_output_types = None
    term_limit = None
    table_format = None
    show_table_formats = None
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
            self.set_class_attr(attr_name, attr_name)
        self.set_pkg_options()
        self._config = Configuration(self.dir, self.config_dir)
        self._cache = Cache()
        self._validate_docstring()

    def _print(self, *args):
        self._config.printer.print(*args)

    def _validate_docstring(self):
        for line_num, line in enumerate(__doc__.splitlines()):
            max_length = Printer.MAX_LINE_LENGTH
            if len(line) > max_length:
                raise docops.ProgramError(
                    f"Docstring line {line_num} "
                    + f"exceeds max line length ({max_length})"
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
        docops.verbose = self.verbose
        docops.quiet = self.quiet
        docops.disable_ansi = self.disable_ansi
        docops.table_format = self.table_format
        docops.term_limit = self.term_limit

    def validate_options(self):
        if self.output_type not in self.OUTPUT_TYPES:
            raise docops.ConfigurationError(
                f"Not a supported type: {self.output_type}"
            )
        if self.table_format not in self.TABLE_FORMATS:
            raise docops.ConfigurationError(
                f"Not a supported type: {self.output_type}"
            )

    def run(self):
        if self.help:
            return self.do_help()
        if not self.show_warnings:
            warnings.filterwarnings("ignore")
        if self.delete_cache:
            return self.do_delete_cache()
        if self.print_cache:
            return self.do_print_cache()
        if self.show_output_types:
            return self.do_show_output_types()
        if self.show_table_formats:
            return self.do_show_table_formats()
        self.validate_options()
        self.do_main()

    def do_help(self):
        self._print(__doc__.strip())
        return 0

    def do_delete_cache(self):
        self._cache.delete_cache()
        return 0

    def do_print_cache(self):
        if not self._cache.print_cache_path():
            return 1
        return 0

    # TODO: Convert most methods of this class to private methods
    def _do_show_options(self, plural_noun, noun_list):
        msg = f"Supported {plural_noun}:\n\n"
        for noun in noun_list:
            if noun:
                msg += f"  - <str>{noun}</str>\n"
        self._print(msg.strip())

    def do_show_output_types(self):
        self._do_show_options("output types", self.OUTPUT_TYPES)

    def do_show_table_formats(self):
        self._do_show_options("table formats", self.TABLE_FORMATS)

    def do_main(self):
        self._config.load()
        self._analyzer = TermAnalyzer(self._config)
        self._analyzer.run()
        if docops.verbose:
            print("Output: {self.output_type}")
        if self.output_type == "table":
            self._analyzer.print_table()
            return
        if self.output_type == "none":
            return
        raise docops.ProgramError("I don't know what to do now...")


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
            args = docopt.docopt(doc, help=False, version=docops.__version__)
        except docopt.DocoptExit as err:
            raise docops.CliError(err)
        command = TermsCommand(args)
        exit_code = command.run()
    except (KeyboardInterrupt, BrokenPipeError):
        # Exit silently when the the user terminates the program early
        pass
    except docops.Error as err:
        printer.print(str(err), sys.stderr)
    sys.exit(exit_code)
