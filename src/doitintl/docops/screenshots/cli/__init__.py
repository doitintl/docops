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
DoiT Screenshots Tool

Usage:
  {entry_point} frame INPUT_IMAGE
  {entry_point} [options] (-h, --help)
  {entry_point} [options] (--version)

Basic options:
  -h, --help      Print this help message and exit
  --version       Print the software version number and exit
  --disable-ansi  Disable ANSI escape code formatting

The `frame` command pastes the `INPUT_IMAGE` on top of the standard template
image and writes out a new file. The reference template image includes a drop
shadow, effectively framing the image.

The  `INPUT_IMAGE` must be exactly 2400 by 1400 pixels, corresponding to 1200
by 700 pixels at macOS retina resolution.
"""

import pathlib
import sys
from doitintl import docops
from doitintl.docops.gitbook import exceptions

import pastel
from docopt import docopt
from PIL import Image


cmd_path = pathlib.PurePath(sys.argv[0])
cmd_name = cmd_path.name


def frame(input_image, disable_ansi=False):
    def print_message(prefix, color, message):
        if not disable_ansi:
            print(
                pastel.colorize(
                    f"<fg={color};options=bold>{prefix}:</> {message}"
                )
            )
        else:
            print(f"{prefix}: {message}")

    input_path = pathlib.Path(input_image)
    template_path = pathlib.Path(__file__).parent / "../assets/frame.png"
    template_path.resolve()

    try:
        input_img = Image.open(input_path)
    except FileNotFoundError:
        print_message("ERROR", "red", "Input file not found")
        sys.exit(1)
    template_img = Image.open(template_path)

    # Check template image is correct size
    if template_img.width != 2560 or template_img.height != 1560:
        print_message("ERROR", "red", "Incorrect template image size")
        sys.exit(1)

    # Check input image is correct size
    if input_img.width != 2400 or input_img.height != 1400:
        print_message("ERROR", "red", "Incorrect input image size")
        sys.exit(1)

    template_img.paste(input_img, (80, 80))

    new_stem = f"{input_path.stem}-out"
    output_path = input_path.with_stem(new_stem)

    template_img.save(output_path, optimize=True)

    print_message("Saved", "green", output_path)


def main(args):
    if args["frame"]:
        frame(args["INPUT_IMAGE"], args["--disable-ansi"])


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
