import pymorphy2
import gensim
import sqlite3
morph = pymorphy2.MorphAnalyzer()

con = sqlite3.connect('recipe.db')
cur = con.cursor()

query1 = """
SELECT ingredients
FROM recipe 
"""
query2 = """
SELECT ingredients, recipe
FROM recipe 
WHERE ingredients = parsedinput 
"""
#ааа а как делать переменную внутри базы? никак?
cur.execute(query)
result = cur.fetchmany()
# print(result)

model_ingr = gensim.models.Word2Vec(result, min_count=1)
x = input()
parsedinput = x.strip().split()
sim = model_ingr.wv.most_similar(parsedinput)
if sim > хх: # типа какое-то число, больше которого должна быть похожесть
