import sqlite3


def search(lst):
    conn = sqlite3.connect("recipe.db")
    cur = conn.cursor()

    lst.sort()
    ing = "%".join(lst)

    execute = """SELECT name,recipe,ingredients FROM recipe  WHERE  ingredients LIKE '%{0}%'""".format(ing)
    cur.execute(execute)
    recipe_lst = cur.fetchall()
    return recipe_lst

    # for r in recipe_lst:
    #     print(r)


# search('recipe.db', ["сахар", "мука"])
