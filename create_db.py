import sqlite3


con = sqlite3.connect('framework_db.sqlite')
cur = con.cursor()

with open('create_db.sql', 'r', encoding='utf-8') as f:
    text = f.read()

cur.executescript(text)
cur.close()
con.close()
