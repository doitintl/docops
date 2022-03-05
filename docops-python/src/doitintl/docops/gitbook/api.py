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


import os

import apiclient
import apiclient.exceptions

from doitintl.docops.gitbook import cache
from doitintl.docops.gitbook import exceptions


class Client(apiclient.APIClient):

    api_token = None
    db = None

    def __init__(self):
        self.api_token = os.environ.get("GITBOOK_API_TOKEN", None)
        if not self.api_token:
            raise exceptions.ClientError(
                "The `GITBOOK_API_TOKEN` environment variable "
                + "has not been set."
            )
        self.db = cache.Database()
        header_auth = apiclient.HeaderAuthentication(token=self.api_token)
        super().__init__(
            authentication_method=header_auth,
            response_handler=apiclient.JsonResponseHandler,
        )

    def whoami(self):
        # TODO: move all of this to the cache, and use the cache as a wrapper
        # for the API not the other way around
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                uid TEXT PRIMARY KEY,
                api_token TEXT NOT NULL,
                title TEXT NOT NULL,
                baseDomain TEXT NOT NULL
            ) WITHOUT ROWID;
        """
        )
        results = self.db.execute(
            "SELECT uid, title, baseDomain FROM users WHERE api_token = ?",
            [self.api_token],
        )
        if results:
            uid, title, baseDomain = results[0]
        else:
            try:
                user = self.get("https://api-beta.gitbook.com/v1/user")
            except apiclient.exceptions.APIClientError as err:
                raise exceptions.ClientError(err)
            uid = user["uid"]
            title = user["title"]
            baseDomain = user["baseDomain"]
            self.db.execute(
                """
                    INSERT INTO users (
                        uid, api_token, title, baseDomain
                    ) VALUES (
                        ?, ?, ?, ?
                    )
                """,
                (
                    uid,
                    self.api_token,
                    title,
                    baseDomain,
                ),
            )
        return f"{title} ({baseDomain})"
