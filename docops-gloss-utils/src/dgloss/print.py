import sys

import pastel

import dgloss


class Printer:
    def __init__(self):
        if dgloss.disable_ansi:
            pastel.with_colors(False)
        else:
            pastel.with_colors(True)

    def print(self, msg, file=sys.stdout):
        msg = pastel.colorize(str(msg))
        msg = f"{msg}\n"
        file.write(msg)
