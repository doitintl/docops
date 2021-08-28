"""GitBook CLI tool

Usage:
  gbclient [options]

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
    dist_name = __package__.split(".")[0]
    dist = pkg_resources.get_distribution(dist_name)
    version = dist.version
    args = docopt(__doc__, version=version)
    try:
        main(args)
    except ClientError as err:
        if not args["--disable-ansi"]:
            err = pastel.colorize(f"<fg=red;options=bold>{err}</>")
        sys.stderr.write(f"{err}\n")
        sys.exit(1)
