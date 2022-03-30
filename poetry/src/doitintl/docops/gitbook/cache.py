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


import pathlib
import sqlite3

import appdirs

from doitintl.docops import gitbook
from doitintl.docops.gitbook import exceptions


class Database:

    # TODO: Use a shared `docops.db` file so tools can easily share data
    _FILENAME = "gitbook.db"

    _db_path = None

    def __init__(self):
        cache_path = gitbook.get_cache_path()
        filename_path = pathlib.Path(self._FILENAME)
        self._db_path = cache_path.joinpath(filename_path)
        return

    def execute(self, query, params=[]):
        con = sqlite3.connect(self._db_path)
        cur = con.cursor()
        try:
            cur.execute(query, params)
            results = cur.fetchall()
        except (sqlite3.Error) as err:
            raise exceptions.DatabaseError(err)
        con.commit()
        con.close()
        return results
