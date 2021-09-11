import os
from urllib import parse
import pathlib
import shutil

import appdirs

import dgloss
from dgloss.print import Printer


class Cache:

    _repo_name = None
    _repo_org = None

    _printer = None

    _cache_path = None
    _db_path = None

    def __init__(self):
        self._printer = Printer()
        project_url = dgloss.__dist__.metadata["Project-URL"]
        # Expect `project_url` to look like "Repository, <URL>"
        repo_url = project_url.split(",")[1].strip()
        repo_url = parse.urlparse(repo_url)
        repo_path = pathlib.PurePosixPath(repo_url.path)
        self._repo_org, self._repo_name = repo_path.parts[1:]
        self._set_cache_path()

    def _print(self, *args):
        self._printer.print(*args)

    def _set_cache_path(self):
        cache_dir = appdirs.user_cache_dir(self._repo_name, self._repo_org)
        cache_path = pathlib.Path(cache_dir)
        self._cache_path = cache_path
        self._make_cache()
        db_filename = pathlib.Path(f"{__name__}.db")
        self._db_path = self._cache_path.joinpath(db_filename)

    def get_cache_path(self):
        return self._cache_path

    def get_db_path(self):
        return self._db_path

    def print_cache_path(self):
        cache_path = self.get_cache_path()
        if os.path.isdir(cache_path):
            self._print(f"{cache_path}")
        else:
            if dgloss.verbose:
                self._print("<fg=yellow>No cache directory found</>")

    def _make_cache(self):
        cache_path = self.get_cache_path()
        if not os.path.isdir(cache_path):
            cache_path.mkdir(parents=True, exist_ok=True)
            self._print(f"<fg=green>Created cache</>: {cache_path}")

    def delete_cache(self):
        cache_path = self.get_cache_path()
        if os.path.isdir(cache_path):
            shutil.rmtree(cache_path)
            if dgloss.verbose:
                self._print(f"<fg=green>Deleted cache</>: {cache_path}")
        else:
            if dgloss.verbose:
                self._print("<fg=yellow>No cache file to delete</>")
