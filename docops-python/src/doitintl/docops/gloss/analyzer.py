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


import gzip
import math
import os
import re
import html
import sqlite3

from tabulate import tabulate

import nltk

from doitintl import docops
from doitintl.docops.gloss import charset

# TODO: For debugging purposes only
import sys
from pprint import pprint


class Analyzer:

    _DROP_LEMMAS_TABLE_QUERY = """
        DROP TABLE IF EXISTS lemmas;
    """

    _DROP_NGRAMS_TABLE_QUERY = """
        DROP TABLE IF EXISTS ngrams;
    """

    _CREATE_LEMMAS_TABLE_QUERY = """
        CREATE TABLE lemmas (
            source TEXT NOT NULL,
            lemma TEXT NOT NULL,
            ipm REAL NOT NULL,
            PRIMARY KEY (source, lemma)
        ) WITHOUT ROWID;
    """

    _CREATE_NGRAMS_TABLE_QUERY = """
        CREATE TABLE ngrams (
            ngram TEXT NOT NULL,
            count INTEGER NOT NULL,
            PRIMARY KEY (ngram)
        ) WITHOUT ROWID;

    """

    _INSERT_LEMMA_QUERY = """
        INSERT OR REPLACE INTO lemmas (
            source, lemma, ipm
        ) VALUES (
            ?, ?, ?
        );
    """

    _INSERT_NGRAM_QUERY = """
        INSERT OR IGNORE INTO ngrams (
            ngram,
            count
        ) VALUES (
            ?,
            ?
        )
    """

    _UPDATE_NGRAM_COUNT_QUERY = """
        UPDATE ngrams SET count = count + 1 WHERE ngram = ?
    """

    _SELECT_DELTAS_QUERY = """
        SELECT
            target.lemma AS lemma,
            IIF(ref.ipm IS NOT NULL, target.ipm - ref.ipm, target.ipm) AS delta
        FROM
            lemmas AS target
        LEFT JOIN
            lemmas AS ref
        ON
            ref.source = 'reference' AND ref.lemma = target.lemma
        WHERE
            target.source = 'target' AND delta > 0
        ORDER BY
            delta DESC
        LIMIT ?;
    """

    _SELECT_NGRAMS_QUERY = """
        SELECT
            ngram,
            count
        FROM
            ngrams
        WHERE
            ngram LIKE '%' || ? || '%'
        ORDER BY
            count DESC
        LIMIT 10;
    """

    _SELECT_NGRAMS_QUERY_TEST = """

        SELECT
            lemmas.lemma as lemma,
            lemmas.delta as delta,
            ngrams.ngram AS ngram,
            ngrams.count as count,
            SUM(lemmas.delta * ngrams.count) AS score
        FROM (
            SELECT
                target.lemma AS lemma,
                IIF(
                    ref.ipm IS NOT NULL, target.ipm - ref.ipm, target.ipm
                ) AS delta
            FROM
                lemmas AS target
            LEFT JOIN
                lemmas AS ref
            ON
                ref.source = 'reference' AND ref.lemma = target.lemma
            WHERE
                target.source = 'target' AND delta > 0
            ORDER BY
                delta DESC
            LIMIT 50
        ) as lemmas
        LEFT JOIN
            ngrams
        WHERE
            ngrams.ngram LIKE '%' || lemmas.lemma || '%'
        GROUP BY
            ngram
        ORDER BY
            score DESC
        LIMIT 50;
    """

    # Hardcoded for now
    _NGRAM_MIN_LENGTH = 2
    _NGRAM_MAX_LENGTH = 5

    _clause_re = re.compile(r"^([.]+|[?]+|[!]+|[,]+|[;]+)$")

    _ngram_tokens = []

    _config = None

    _db_cursor = None

    def __init__(self, config):
        # Load configuration before continuing
        self._config = config

    def _print(self, *args, **kwargs):
        self._config._printer.print(*args, **kwargs)

    def _create_schema(self):
        if docops._get_more_verbose():
            self._print("<warning>Resetting cache...</warning>")
        self._db_cursor.execute(self._DROP_LEMMAS_TABLE_QUERY)
        self._db_cursor.execute(self._DROP_NGRAMS_TABLE_QUERY)
        self._db_cursor.execute(self._CREATE_LEMMAS_TABLE_QUERY)
        self._db_cursor.execute(self._CREATE_NGRAMS_TABLE_QUERY)

    def _load_pkg_corpus(self, corpus):
        corpus_name = corpus["name"]
        if not docops._get_quiet():
            self._print(
                "<info>Loading word frequency corpus</info>: ", corpus_name
            )
        with gzip.open(corpus["abs_filename"], "rb") as f:
            bytes = f.read()
        text = charset.decode_bytes(bytes, filename=corpus["data_filename"])
        line_re = re.compile(corpus["re"])
        source = "reference"
        for line in text.splitlines():
            matches = line_re.match(line.strip())
            if not matches:
                continue
            ipm = float(matches.group("ipm"))
            lemma = matches.group("lemma")
            lemma = self._config.get_lemmatizer().lemmatize(lemma)
            lemma = self._filter_lemma(lemma)
            if not lemma:
                continue
            self._db_cursor.execute(
                self._INSERT_LEMMA_QUERY, [source, lemma, ipm]
            )
            if docops._get_max_verbose():
                self._print(f"<success>Added to {source}</success>: ", lemma)

    def _load_pkg_corpora(self):
        # TODO: Raise custom exception if dict key not found
        corpora = self._config._word_frequency_corpora
        if not corpora:
            raise docops.ConfigurationError(
                "No word frequency corpus specified"
            )
        for corpus in corpora:
            self._load_pkg_corpus(corpus)

    def _scan_dir(self):
        dirname = self._config._target_dirname
        if docops._get_verbose():
            self._print("<info>Scanning target directory</info>: ", dirname)
        lemmas_counts = {}
        total_lemma_count = 0
        for root, dirs, files in os.walk(dirname):
            # Skip directories starting with `.`
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for filename in files:
                # Skip files starting with `.`
                if filename.startswith("."):
                    continue
                filename = os.path.join(root, filename)
                lemma_count = self._scan_file(filename, lemmas_counts)
                total_lemma_count += lemma_count
        self._process_lemmas(lemmas_counts, total_lemma_count)

    # TODO: Refactor this method to split up lemma and ngram processing
    def _scan_file(self, filename, lemmas_counts):
        if not docops._get_quiet():
            self._print("<info>Scanning</info>: ", filename)
        try:
            text = charset.decode_file(filename)
        except docops.EncodingError:
            if docops._get_verbose():
                self._print("<warningw>Skipped</warning>", filename)
            # Return a count of zero lemmas
            return 0
        tokens = nltk.word_tokenize(text)
        total_lemma_count = 0
        for token in tokens:
            self._add_ngram_token(token)
            lemma = self._config.get_lemmatizer().lemmatize(token)
            lemma = self._filter_lemma(lemma)
            if not lemma:
                continue
            count = lemmas_counts.get(lemma, 0)
            lemmas_counts[lemma] = count + 1
            total_lemma_count += 1
        return total_lemma_count

    def _add_ngram_token(self, token):
        # Reset the accumulator at the end of every clause
        if self._clause_re.fullmatch(token):
            self._ngram_tokens = []
            return False
        # Ignore non-alphanumeric tokens
        if not token.isalnum():
            return False
        if not self._config._ngrams_case_sensitive:
            token = token.lower()
        self._ngram_tokens.append(token)
        if len(self._ngram_tokens) > self._NGRAM_MAX_LENGTH:
            self._ngram_tokens.pop(0)
        for i in range(self._NGRAM_MIN_LENGTH, self._NGRAM_MAX_LENGTH + 1):
            ngram_tokens = self._ngram_tokens[0:i]
            ngram_str = " ".join(ngram_tokens)
            if len(ngram_tokens) == i:
                self._insert_ngram_tokens(ngram_tokens)
                if docops._get_max_verbose():
                    self._print(
                        "<success>Updated ngram count for:</success> ",
                        ngram_str,
                    )
            else:
                if docops._get_max_verbose():
                    self._print(
                        "<warning>Ignoring ngram:</warning> ", ngram_str
                    )
        return True

    def _insert_ngram_tokens(self, ngram_tokens):
        # for token in ngram_tokens:
        #     if token in self._config._ignore_stopwords:
        #         return
        ngram = " ".join(ngram_tokens)
        self._db_cursor.execute(self._INSERT_NGRAM_QUERY, [ngram, 1])
        self._db_cursor.execute(self._UPDATE_NGRAM_COUNT_QUERY, [ngram])

    def _filter_lemma(self, lemma):
        if not self._config._lemmas_case_sensitive:
            lemma = lemma.lower()
        for regex in self._config._lemmas_ignore_set:
            if regex.search(lemma):
                if docops._get_more_verbose():
                    self._print("<warning>Ignoring:</warning> ", lemma)
                return None
        return lemma

    def _process_lemmas(self, lemmas_counts, total_lemma_count):
        source = "target"
        for lemma, count in lemmas_counts.items():
            percent = count / total_lemma_count
            ipm = round(percent * 1000000, 2)
            self._db_cursor.execute(
                self._INSERT_LEMMA_QUERY, [source, lemma, ipm]
            )
            if docops._get_verbose():
                if len(lemma) > 40:
                    lemma = lemma[:40] + "[...]"
                self._print(f"<success>Added to {source}:</success>: ", lemma)

    def _db_get_cursor(self):
        if docops._get_max_verbose():
            self._print("<info>Establishing database connection...</info>")
        db_path = self._config._cache.get_db_path()
        self._db_connection = sqlite3.connect(db_path)
        self._db_cursor = self._db_connection.cursor()

    def _db_commit_and_close(self):
        if docops._get_max_verbose():
            self._print("<info>Commiting database changes...</info>")
        self._db_connection.commit()
        if docops._get_max_verbose():
            self._print("<info>Closing database connection...</info>")
        self._db_connection.close()

    def run(self):
        self._db_get_cursor()
        self._create_schema()
        self._load_pkg_corpora()
        self._scan_dir()
        self._db_commit_and_close()

    def print_table(self):
        table_format = docops._get_table_format()
        if docops._get_verbose():
            self._print("<info>Table format:</info> ", table_format)

        self._db_get_cursor()

        # Original table code
        # limit = docops._get_term_limit()
        # query_rows = self._db_cursor.execute(
        #     self._SELECT_DELTAS_QUERY, [limit]
        # )
        # lemma_rows = []
        # for query_row in query_rows:
        #     lemma, delta = query_row
        #     rank = round(math.log(delta))
        #     lemma_rows.append([rank, lemma])
        # headers = ["Rank", "Base term"]
        # table = tabulate(lemma_rows, headers=headers, tablefmt=table_format)
        # self._print(table)

        query_rows = self._db_cursor.execute(self._SELECT_NGRAMS_QUERY_TEST)
        table_rows = []
        for query_row in query_rows:
            lemma, delta, ngram, count, score = query_row
            rank = round(math.log(delta))
            score = round(math.log(score))
            table_rows.append([lemma, rank, ngram, count, score])
        headers = [
            "Key term",
            "Term rank",
            "Phrase",
            "Phrase count",
            "Priority",
        ]
        table = tabulate(table_rows, headers=headers, tablefmt=table_format)
        if not docops._get_quiet():
            print()
        self._print(table)

        # THIS WORKS!
        # ngram_rows = []
        # for table_row in lemma_rows:
        #     rank, lemma = table_row
        #     query_rows = self._db_cursor.execute(
        #         self._SELECT_NGRAMS_QUERY, [lemma]
        #     )
        #     for query_row in query_rows:
        #         ngram, count = query_row
        #         ngram_rows.append([rank, lemma, ngram, count])

        # headers = ["Rank", "Base term", "Ngram", "Count"]
        # table = tabulate(ngram_rows, headers=headers, tablefmt=table_format)
        # self._print(table)

        self._db_commit_and_close()
