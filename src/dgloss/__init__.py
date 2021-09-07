from importlib import metadata

__dist__ = metadata.distribution("doit-gloss-utils")
__version__ = __dist__.version

verbose = False
quiet = False
disable_ansi = False
