from bs4 import BeautifulSoup
from urllib import request, parse
import time
import re

def scrape_anythings(url):
    time.sleep(2)
    response = request.urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    response.close()
    recipes = []
    recipe = ''

    # 好きなように名前変更してください
    # レシピ名
    recipeName = soup.find('h1', class_='break-words text-cookpad-16 xs:text-cookpad-24 lg:text-cookpad-36 font-semibold leading-tight clear-both')
    # 作者コメント
    autherComment = soup.find('div', class_='relative break-words text-cookpad-14 bg-cookpad-gray-300 print:bg-transparent rounded-lg p-rg pb-sm print:p-0 lg:hidden')
    # 材料
    material = soup.find('div', class_='flex flex-col space-y-rg bg-cookpad-white lg:rounded-lg lg:shadow p-rg mb-sm lg:px-0 lg:pt-0 lg:shadow-none lg:pb-md lg:mb-md p-rg w-full lg:sticky top-header lg:top-sidebar-header lg:-mt-sm lg:pt-sm lg:min-w-40 print:block print:max-h-full print:px-0 print:space-y-sm lg:max-h-[calc(100vh-132px)]')
    # 作り方
    how = soup.find('div', class_='flex flex-col space-y-rg bg-cookpad-white lg:rounded-lg lg:shadow p-rg mb-sm lg:px-0 lg:pt-0 lg:shadow-none lg:pb-md lg:mb-md lg:border-b print:border-none border-cookpad-gray-300 lg:rounded-none print:px-0 print:pb-0')
    # 作り方のコツ
    advice = soup.find('div', class_='flex flex-col space-y-rg bg-cookpad-white lg:rounded-lg lg:shadow p-rg mb-sm lg:px-0 lg:pt-0 lg:shadow-none lg:pb-md lg:mb-md lg:border-b print:border-none border-cookpad-gray-300 lg:rounded-none print:px-0 print:pb-0')
    # つくれぽ
    report = soup.find('div', class_='flex flex-col space-y-rg bg-cookpad-white lg:rounded-lg lg:shadow p-rg mb-sm print:hidden lg:px-0 lg:pt-0 lg:shadow-none lg:pb-md lg:mb-md lg:border-b print:border-none border-cookpad-gray-300 lg:rounded-none p-rg')
    if recipeName:
        recipe += ('Name:' + (recipeName.text.strip()) + ',') # .strip()で前後の余白を削除
    if autherComment:
        recipe += ('AutherComment:' + (autherComment.text.strip()) + ',')
    if(material):
        recipe += ('Material:' + (material.text.strip()) + ',')
    if(how):
        recipe += ('How:' + (how.text.strip()) + ',')
    if(advice):
        recipe += ('Advice:' + (advice.text.strip()) + ',')
    if(report):
        recipe += ('Report:' + (report.text.strip()))
    cleaned_recipe = re.sub(r'\n', '', recipe)
    recipes.append(cleaned_recipe)

    return recipes

def scrape_cookpad(search_query):
    time.sleep(2)
    encoded_query = parse.quote(search_query)
    search_url = f'https://cookpad.com/jp/search/{encoded_query}'
    response = request.urlopen(search_url)
    soup = BeautifulSoup(response, 'html.parser')
    response.close()

    recipes = soup.find_all('div', class_='flex-auto m-rg')

    allRecipe = []
    # ここで持ってくるデータの数を変える
    for recipe in recipes[:1]:
        a_tag = recipe.find('a')
        if a_tag and 'href' in a_tag.attrs:
            full_url = f'https://cookpad.com{a_tag["href"]}'
            allRecipe.append(scrape_anythings(full_url))

    return allRecipe
