import sqlite3


def write_to_db(name, recipe):
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    cur.execute("INSERT INTO recipe (name, ingredients, recipe) VALUES (?, ?, ?)", (recipe['name'], ' '.join(recipe['ingredients']), recipe['recipe']))
    conn.commit()
