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


"""
DoiT GitBook Client

Usage:
  {entry_point} [options] (-h, --help)
  {entry_point} [options] (--version)
  {entry_point} [options] (--test-env)
  {entry_point} [options] (--whoami)

Basic options:
  -h, --help      Print this help message and exit
  --version       Print the software version number and exit
  --disable-ansi  Disable ANSI escape code formatting
  --test-env      Test for the `GITBOOK_API_TOKEN` environment variable

User options:
  --whoami        Print information about the currently authenticated GitBook
                  user
"""

import sys
import pathlib

from docopt import docopt

import pastel

from doitintl import docops
from doitintl.docops.gitbook import api
from doitintl.docops.gitbook import cache
from doitintl.docops.gitbook import exceptions


cmd_path = pathlib.PurePath(sys.argv[0])
cmd_name = cmd_path.name


def test_env():
    client = api.Client()
    print(f"Your API token is: {client.api_token}")


def whoami():
    client = api.Client()
    print(client.whoami())
    return


def main(args):
    if args["--test-env"]:
        test_env()
    if args["--whoami"]:
        whoami()


def run():
    doc = __doc__.format(entry_point=cmd_name)
    args = docopt(doc, version=docops.__version__)
    try:
        main(args)
    except exceptions.ClientError as err:
        if not args["--disable-ansi"]:
            err = pastel.colorize(f"<fg=red;options=bold>{err}</>")
        sys.stderr.write(f"{err}\n")
        sys.exit(1)
