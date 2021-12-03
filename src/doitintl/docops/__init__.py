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


import os
from posixpath import dirname
import sys
import pathlib
import inspect

from importlib.metadata import distribution

import inflection
from pkg_resources import resource_filename

__dist__ = distribution("doitintl-docops")
__version__ = __dist__.version


# The path to the root Python source code directory for this module
src_path = pathlib.Path(__file__).parent
data_path = src_path.joinpath("data")

verbose = False
quiet = False
disable_ansi = False
term_limit = 50
table_format = "simple"

# TODO: Document this in the developer ops and integrate it into the
# `launch.json`config
debug = bool(os.environ.get("DOCOPS_DEBUG", None))

# The standard UNIX file-parsing error outputs are:
#
#     file_name:line:column: message
#     file_name:line: message


# TODO: Make more use of this function
def print_debug(msg):
    fn_name = None
    caller = inspect.currentframe().f_back
    frame = inspect.getframeinfo(caller)
    path = pathlib.Path(frame.filename)
    path = path.relative_to(src_path)
    line_num = frame.lineno
    fn_name = frame.function
    caller = caller.f_back
    # Format the text using a lighter shade (if supported)
    context = f"\x1b[00;2m{path}:{line_num} {fn_name} -\x1b[0m"
    msg = f"\x1b[00;1m{msg}\x1b[0m\n"
    output = f"{context} {msg}"
    sys.stderr.write(output)
    sys.stderr.flush()


class Error(Exception):

    err = None

    def __str__(self, no_prefix=False):
        self.err = super().__str__()
        if no_prefix:
            return self.err
        error_type = self.get_error_type()
        return f"<error>{error_type}</error>: {self.err}"

    def get_error_type(self):
        error_type = self.__class__.__name__
        error_type = inflection.underscore(error_type)
        error_type = inflection.humanize(error_type)
        error_type = error_type.upper()
        return error_type


class NotImplementedError(Exception):

    pass


class ProgramError(Error):

    pass


class EncodingError(Error):

    pass


class UserError(Error):
    pass


class CliError(UserError):
    def __str__(self):
        # Let docopt print it's own error without an error prefix
        return super().__str__(no_prefix=True)


class ConfigurationError(UserError):

    pass


class ParseError(ConfigurationError):

    _parse_errors = None

    def __init__(self, parse_errors=[]):
        super().__init__()
        self._parse_errors = parse_errors

    def __str__(self):
        output = ""
        for parse_error in self._parse_errors:
            filename, line_num, msg = parse_error
            output += f"{filename}:{line_num}: {msg}\n"
        if verbose:
            error_type = self.get_error_type()
            output = f"<error{error_type}</error>:\n\n{output}"
        output = output.strip()
        return output
