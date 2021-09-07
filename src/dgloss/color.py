import sys

import pastel

import dgloss


class Formatter:
    def __init__(self):
        if dgloss.disable_ansi:
            pastel.with_colors(False)
        else:
            pastel.with_colors(True)

    def print(self, msg, stdout=True):
        msg = pastel.colorize(msg)
        msg = f"{msg}\n"
        if stdout:
            sys.stdout.write(msg)
        else:
            sys.stderr.write(msg)
