import pandas as pd
from scrap_book import book_request, catch_book_data
import math
from pathlib import Path

def catch_categories_url(category_url):
    """ Recuperation des urls de chaque categories"""
    
    print('Etape 4 : catch_categories_url')
    categories_url = []
    page = check_pages(category_url)
    if page == 1:
        categories_url.append(category_url)
    else:
        for i in range(page):
            page_url = category_url.replace("index.", f"page-{i+1}.")
            print('Extraction de la page : ', page_url)
            categories_url.append(page_url)
    return categories_url

def check_pages (categories_url):
    """ Verification du nombre de pages présentes dans la catégorie"""

    print('Etape 5 check pages')
    content = book_request(categories_url)
    number_element_page = content.select("strong")[1].text
    page_in_int = int(number_element_page)
    division_pages = page_in_int/20
    number_of_page = math.ceil(division_pages)
    print('Nombre de page présente ', number_of_page)
    return number_of_page

def catch_book_urls(categories_url):

    books_url = []
    print('Etape 4 catch_book_urls')
    for category_url in categories_url:
        content = book_request(category_url)
        titles = content.find_all("h3")
        for title in titles:
            href = title.find('a')["href"]
            if "../../.." in href:
                url = href.replace(
                    "../../../", "http://books.toscrape.com/catalogue/")
            else:
                url = "http://books.toscrape.com/" + href

            books_url.append(url)
    print(books_url)
    return books_url

def save_book_data(category_url):
    
    books_data = []
    categories = catch_categories_url(category_url)
    books_url = catch_book_urls(categories)

    for url in books_url:
        print(url)
        book = catch_book_data(url)
        books_data.append(book)

        file_name = books_data[0]["category"]
        folder = Path(f"data\{file_name}")
        folder.mkdir(parents=True, exist_ok=True)
    
    print('Sauvegarde de : ',file_name)
    pd.DataFrame(books_data).to_csv(f'data/{file_name}/{file_name}.csv', encoding = 'utf-8')
    
    return file_name, books_data