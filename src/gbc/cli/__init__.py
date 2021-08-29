"""GitBook API Client

Usage:
  {entry_point} [options] (-h, --help)
  {entry_point} [options] (--version)
  {entry_point} [options] (--test-env)

Options:
  -h, --help      Print this help message and exit
  --version       Print the software version number and exit
  --disable-ansi  Disable ANSI escape code formatting
  --test-env      Test for the `GITBOOK_API_TOKEN` environment variable
"""

import sys
import os
import pkg_resources

from docopt import docopt

import pastel

from gbc import __dist__, __version__

console_scripts = __dist__.get_entry_map()["console_scripts"]
for name, entry_point in console_scripts.items():
    if entry_point.module_name == __name__:
        __entry_point__ = name


class ClientError(Exception):
    pass


def get_api_token():
    api_token = os.environ.get("GITBOOK_API_TOKEN", None)
    if not api_token:
        raise ClientError(
            "The `GITBOOK_API_TOKEN` environment variable has not been set."
        )
    return api_token


def test_env():
    api_token = get_api_token()
    print(f"Your API token is: {api_token}")


def main(args):
    if args["--test-env"]:
        test_env()


def run():
    doc = __doc__.format(entry_point=__entry_point__)
    args = docopt(doc, version=__version__)
    try:
        main(args)
    except ClientError as err:
        if not args["--disable-ansi"]:
            err = pastel.colorize(f"<fg=red;options=bold>{err}</>")
        sys.stderr.write(f"{err}\n")
        sys.exit(1)
