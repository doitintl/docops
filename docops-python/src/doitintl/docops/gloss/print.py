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


import sys

import pastel

from doitintl import docops

# For the full list of options, see:
# https://github.com/sdispater/pastel/blob/master/pastel/style.py


class Printer(pastel.Pastel):

    MAX_LINE_LENGTH = 79

    # TODO: Make use of these throughout the code
    STYLES = {
        "success": {
            "fg": "green",
            "options": None,
        },
        "error": {
            "fg": "red",
            "options": ["bold"],
        },
        "warning": {
            "fg": "yellow",
        },
        # Value types
        "type": {
            "options": ["bold"],
        },
        # Numeric values
        "num": {
            "fg": "magenta",
        },
        # String values
        "str": {
            "fg": "cyan",
        },
        # Object values
        "obj": {
            "options": ["dark"],
        },
        "emphasis": {
            "options": ["italic"],
        },
        "strong": {
            "options": ["bold"],
        },
        "special": {
            "options": ["underline"],
        },
    }

    def __init__(self):
        super().__init__()
        self.with_colors(not docops.disable_ansi)
        self._configure_styles()

    def _configure_styles(self):
        for name, kwargs in self.STYLES.items():
            self.add_style(name, **kwargs)

    def print(self, msg, file=sys.stdout):
        msg = self.colorize(str(msg))
        msg = f"{msg}\n"
        file.write(msg)
