import os
from urllib import parse
import pathlib
import shutil

import appdirs

import dgloss
from dgloss.color import Formatter


class Configuration:

    _repo_name = None
    _repo_org = None

    _formatter = None

    cache_path = None

    def __init__(self):
        self._formatter = Formatter()
        project_url = dgloss.__dist__.metadata["Project-URL"]
        # Expect `project_url` to look like "Repository, <URL>"
        repo_url = project_url.split(",")[1].strip()
        repo_url = parse.urlparse(repo_url)
        repo_path = pathlib.PurePosixPath(repo_url.path)
        self._repo_org, self._repo_name = repo_path.parts[1:]

    def _print(self, msg, stdout=True):
        self._formatter.print(msg, stdout)

    def set_cache_path(self):
        cache_dir = appdirs.user_cache_dir(self._repo_name, self._repo_org)
        cache_path = pathlib.Path(cache_dir)
        self.cache_path = cache_path
        return self.cache_path

    def print_cache_path(self):
        cache_path = self.set_cache_path()
        if os.path.isdir(cache_path):
            self._print(f"{cache_path}")
        else:
            if dgloss.verbose:
                self._print(f"<fg=yellow>No cache directory found</>")

    def make_cache(self):
        cache_path = self.set_cache_path()
        if not os.path.isdir(cache_path):
            cache_path.mkdir(parents=True, exist_ok=True)
            self._print(f"<fg=green>Created cache</>: {cache_path}")
        return cache_path

    def delete_cache(self):
        cache_path = self.set_cache_path()
        if os.path.isdir(cache_path):
            shutil.rmtree(cache_path)
            if dgloss.verbose:
                self._print(f"<fg=green>Deleted cache</>: {cache_path}")
        else:
            if dgloss.verbose:
                self._print(f"<fg=yellow>No cache file to delete</>")
