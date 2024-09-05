from bs4 import BeautifulSoup
from urllib import request, parse
import time

def scrape_cookpad(search_query):
    encoded_query = parse.quote(search_query)
    search_url = f'https://cookpad.com/jp/search/{encoded_query}'
    response = request.urlopen(search_url)
    soup = BeautifulSoup(response, 'html.parser')
    response.close()

    recipes = soup.find_all('div', class_='flex-auto m-rg')
    recipe_list = [str(recipe) for recipe in recipes[:5]]  # 最初の5つのみ取得

    time.sleep(3)

    return recipe_list
