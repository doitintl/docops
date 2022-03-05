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
_src_path = pathlib.Path(__file__).parent
_data_path = _src_path.joinpath("data")

_debug = False
_verbose = False
_more_verbose = False
_max_verbose = False
_quiet = False
_disable_ansi = False
_term_limit = 50
_table_format = "grid"

# TODO: Ugh this whole thing needs some serious refactoring


def _get_data_path():
    return _data_path


def _get_debug():
    return _debug


def _get_verbose():
    return _verbose


def _get_more_verbose():
    return _verbose or _more_verbose


def _get_max_verbose():
    return _verbose or _more_verbose or _max_verbose


def _get_quiet():
    return _quiet


def _get_disable_ansi():
    return _disable_ansi


def _get_term_limit():
    return _term_limit


def _get_table_format():
    return _table_format


# TODO: Document this in the developer ops and integrate it into the

_debug = False
# `launch.json`config
if os.environ.get("DOCOPS_DEBUG", None):
    _debug = True

# The standard UNIX file-parsing error outputs are:
#
#     file_name:line:column: message
#     file_name:line: message


# TODO: Make more use of this function
# def print_debug(msg):
#     fn_name = None
#     caller = inspect.currentframe().f_back
#     frame = inspect.getframeinfo(caller)
#     path = pathlib.Path(frame.filename)
#     path = path.relative_to(src_path)
#     line_num = frame.lineno
#     fn_name = frame.function
#     caller = caller.f_back
#     # Format the text using a lighter shade (if supported)
#     context = f"\x1b[00;2m{path}:{line_num} {fn_name} -\x1b[0m"
#     msg = f"\x1b[00;1m{msg}\x1b[0m\n"
#     output = f"{context} {msg}"
#     sys.stderr.write(output)
#     sys.stderr.flush()


class Error(Exception):

    no_prefix = None

    def get_prefix(self):
        if self.no_prefix:
            return ""
        error_type = self.get_error_type()
        return f"<error>{error_type}</error>: "

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
    # Let docopt print it's own error without an error prefix
    def get_prefix(self):
        return None


class ConfigurationError(UserError):

    pass
