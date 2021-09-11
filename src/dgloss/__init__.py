import os
import pathlib

from importlib.metadata import distribution

import inflection
from pkg_resources import resource_filename

__dist__ = distribution("doit-gloss-utils")
__version__ = __dist__.version


def get_pkg_path(path):
    pkg_root_path = "../../"
    path = os.path.join(pkg_root_path, path)
    path = resource_filename(__name__, path)
    path = os.path.abspath(path)
    path = pathlib.Path(path)
    return path


editorconfig_path = get_pkg_path(".editorconfig")
data_path = get_pkg_path("data")

verbose = False
quiet = False
disable_ansi = False
row_limit = 100
table_format = "simple"


class Error(Exception):

    err = None

    def __str__(self, no_prefix=False):
        self.err = super().__str__()
        if no_prefix:
            return self.err
        error_type = self.get_error_type()
        return f"<fg=red>{error_type}</>: {self.err}"

    def get_error_type(self):
        error_type = self.__class__.__name__
        error_type = inflection.underscore(error_type)
        error_type = inflection.humanize(error_type)
        error_type = error_type.upper()
        return error_type


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
        # The standard UNIX file-parsing error outputs are:
        #
        #     file_name:line:column: message
        #     file_name:line: message
        output = ""
        for parse_error in self._parse_errors:
            filename, line_num, msg = parse_error
            output = output + f"{filename}:{line_num}: {msg}\n"
        if verbose:
            error_type = self.get_error_type()
            output = f"<fg=red>{error_type}</>:\n\n{output}"
        output = output.strip()
        return output
