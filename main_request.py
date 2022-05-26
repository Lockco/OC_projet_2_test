from bs4 import BeautifulSoup as bs
from scrap_category import save_book_data
from scrap_book import book_request
import requests
import re
from pathlib import Path

URL = "http://books.toscrape.com/"


def catch_all_page_catalogue(url):
    """ Recuperation des 50 pages du catologue pour récupérer les images"""

    page = 1
    pages_url = []

    
    while True:
    #
        page_url = (url +'catalogue/' + f"page-{page}.html")
        page += 1
        response = requests.get(page_url)
        if response.status_code == 200:
            pages_url.append(page_url)
        else:
            break
    return pages_url

def extraction(url):

    print("Etape 2 : Extraction")
    all_category = []
    soup = book_request(url)
    all_ul = soup.find('div', class_="side_categories").find('ul').find_all('li')[1:]
    for category_url in all_ul:
        href = category_url.find("a")["href"]
        url = URL+("/")+href
        all_category.append(url)
    return all_category

def catch_images(url):
    """ Recuperation des images"""

    page_url = catch_all_page_catalogue(url)
    folder = Path("data/images/")
    folder.mkdir(parents=True, exist_ok=True)
    for links in page_url:
        print('Extraction de la page : ', links)
        result = requests.get(links)
        content = result.text
        content_page = bs(content, 'lxml')
        images = content_page.find_all('img')
        

        for image in images:
            name = image['alt']
            url =(URL + image['src'])
            print(name)
            name = re.sub(r"['\"[\]{}()?\-\+*&é;:./!,$=#]*","",name)
            print('nouveau nom',name)
            with open((f"data\images\{name}.jpg"), 'wb') as f:
                f.write(requests.get(url).content)

def main(url):
    print('Extraction en cours : ')
    print('Etape 1 = Départ')
    all_products = []
    list_url = extraction(url)
    print(url)
    for url in list_url:
        save_book_data(url)