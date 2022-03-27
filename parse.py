import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import List
from create_db import create_database
from write_to_db import write_to_db


class Recipe(BaseModel):
    name: str
    recipe: str
    ingredients: List[str]


def crawler(url):
    ua = UserAgent(verify_ssl=False)
    headers = {'User-Agent': ua.random}
    session = requests.session()
    req = session.get(url, headers=headers)
    page = req.text
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def parse_page(url):
    soup = crawler(url=url)
    links = soup.find_all('div', {'class': 'cooking-bl', 'itemprop': 'recipeInstructions'})
    recipe_list = []
    for t in links:
        recipe_list.append(t.text.replace('\n', ''))

    recipe_text = ' '.join(recipe_list)
    return recipe_text


def parse_site(url):
    soup = crawler(url)
    links = soup.find_all('article', {'class': 'item-bl'})

    for item in links:
        ingredients = []
        list_ingredients = item.find_all('span', {'class': 'list'})[0].find_all('a')
        for ingredient in list_ingredients:
            ingredients.append(ingredient.text)

        recipe_text = parse_page(item.div.a.get('href'))

        recipe = Recipe(
            name=item.h2.a.text,
            ingredients=ingredients,
            recipe=recipe_text,
        )
        # print(recipe.dict())
        # parse_page(item.div.a.get('href'))
        if recipe_text == '':
            continue
        else:
            write_to_db(name_db, recipe.dict())
        print(recipe.dict())


def main():
    global name_db
    name_db = "recipe.db"
    create_database(name_db)
    for i in range(1, 100):
        url = f"https://www.povarenok.ru/recipes/~{i}"
        parse_site(url=url)


if __name__ == "__main__":
    main()
