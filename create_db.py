import sqlite3


def create_database(name):
    conn = sqlite3.connect(name)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS recipe
    (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, ingredients text, recipe text)
    """)

    conn.commit()
    conn.close()
