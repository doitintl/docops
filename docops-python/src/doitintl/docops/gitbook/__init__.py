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


from urllib import parse
import pathlib

import appdirs

from doitintl import docops


def get_cache_path(ensure_exists=True):
    project_url = docops.__dist__.metadata["Project-URL"]
    # Expect `project_url` to look like "Repository, <URL>"
    repo_url = project_url.split(",")[1].strip()
    repo_url = parse.urlparse(repo_url)
    repo_path = pathlib.PurePosixPath(repo_url.path)
    repo_org, repo_name = repo_path.parts[1:]
    cache_dir = appdirs.user_cache_dir(repo_name, repo_org)
    cache_path = pathlib.Path(cache_dir)
    if ensure_exists:
        cache_path.mkdir(parents=True, exist_ok=True)
    return cache_path
