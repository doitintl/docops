import sys
import sqlite3

from tabulate import tabulate

import spacy
import pytextrank

from icecream import ic


DROP_TABLE_QUERY = """
    DROP TABLE IF EXISTS noun_chunks;
"""

DROP_TABLE_QUERY = """
    DROP TABLE IF EXISTS ents;
"""


DROP_TABLE_QUERY = """
    DROP TABLE IF EXISTS phrases;
"""

CREATE_TABLE_QUERY = """
    CREATE TABLE phrases (
        phrase TEXT NOT NULL,
        rank REAL NOT NULL,
        count REAL NOT NULL,
        PRIMARY KEY (phrase)
    ) WITHOUT ROWID;
"""

INSERT_QUERY = """
    INSERT OR REPLACE INTO phrases (
        phrase, rank, count
    ) VALUES (
        ?, ?, ?
    );
"""

SELECT_QUERY = """
    SELECT
        phrase,
        rank,
        count
    FROM
        phrases
    ORDER BY
        count DESC
    LIMIT ?;
"""


text = open("text.txt").read()
nlp = spacy.load("en_core_web_sm")

# nlp.add_pipe("textrank", config={ "stopwords": { "word": ["NOUN"] } })

# nlp.add_pipe("textrank")

# nlp.add_pipe("positionrank")

# nlp.add_pipe("biasedtextrank")

doc = nlp(text)

# for p in doc._.phrases:
#     ic(p.rank, p.count, p.text)
#     ic(p.chunks)

# for chunk in doc.noun_chunks:
#     ic(chunk.text)

# for ent in doc.ents:
#     ic(ent.text, ent.label_, ent.start, ent.end)

# for phrase in doc._.phrases[:100]:
#     ic(phrase)

sys.exit(0)

con = sqlite3.connect("sqlite.db")
cur = con.cursor()
cur.execute(DROP_TABLE_QUERY)
cur.execute(CREATE_TABLE_QUERY)

for phrase in doc._.phrases:
    cur.execute(INSERT_QUERY, [phrase.text, phrase.rank, phrase.count])

headers = ["Phrase", "Rank", "Score"]
table_rows = []
for row in cur.execute(SELECT_QUERY, [100]):
    table_rows.append(row)

con.commit()
con.close()

table = tabulate(table_rows, headers=headers, tablefmt="simple")

print(table)
