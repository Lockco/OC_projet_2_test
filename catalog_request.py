from this import d
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd



URL = 'https://books.toscrape.com/catalogue/finders-keepers-bill-hodges-trilogy-2_807/index.html'
response = requests.get(URL)

if response.status_code != 200:
    print("le site ne répond pas")
else:
    catalogue_contents = response.text

doc = bs(response.text,'html.parser')


def catch_book_titles(doc):
    """Recuperation des titres"""

    Book_title = doc.find_all('h1')
    Book_titles = []

    for title in Book_title:
        Book_titles.append(title.text)
        print(Book_titles)
    return Book_titles

def catch_book_price(doc):
    """Recuperation du prix"""

    Book_price_tags = doc.find('p', class_='price_color')
    Book_price = []

    for tags in Book_price_tags:
        Book_price.append(tags.text.replace('Â', ''))

    return Book_price

def catch_description(doc):
    """Recuperation de la description"""

    description_book = doc.find('article', class_='product_page')
    descriptions = description_book.find_all('p')
    list_desc = []
    list_desc.append(descriptions[3].text)

    return list_desc

def catch_rating(doc):
    """Recuperation des notes du livre"""

    doc.find_all('div', class_="col-sm-6 product_main")
    rating = doc.select("p:nth-of-type(3)")[0].get('class')[1]
  
    return rating

def catch_img_url(doc):
    """Recuperation de l'url de l'image"""

    item = doc.find('div', class_='item active')
    img = item.findAll('img')
    link_img = img[0]
    img_url = link_img.attrs['src']
    url = img_url.replace('../../','')
    full_img_url = ('https://books.toscrape.com/' + url)

    return full_img_url

def catch_product_page_url(doc):
    """Recuperation de l'url de la page"""

    product_page_book = doc.find('div', class_='content')
    print(len(product_page_book))
    product_item = product_page_book.select('a')[0]
    print(product_item)
    product_page = product_page_book.find('a')
    print(product_page)
    product = product_page.attrs['href']
    print(product)
    product_url = product.replace('../','')
    url_product = ('https://books.toscrape.com/catalogue/' + product_url)

    return url_product

def catch_book_category(doc):
    """Recuperation de la categorie du livre"""
    category_book = doc.find('ul', class_='breadcrumb')
    categorys = category_book.find_all('a')
    category_name = []
    category_name.append(categorys[2].text)
    print(category_name)

    return category_name

def export_data_csv(doc):
    """Export des donnees recuperees au format .csv """

    table = doc.find("table", attrs={'class': 'table table-striped'})
    results = table.find_all('td')

    results_table = []

    for result in results:
        results_table.append(result.text.replace('Â', ''))

    results_table.extend(catch_book_titles(doc))
    results_table.extend([catch_img_url(doc)])
    results_table.extend([catch_product_page_url(doc)])
    results_table.extend([catch_description(doc)])
    results_table.extend([catch_rating(doc)])
    
    print(len(results_table))

    informations_list = (results_table)

    info_list = pd.DataFrame([informations_list], columns = ['universal_ product_code (upc)', 'category' , 'price_excluding_tax', 'price_including_tax', 'Taxes', 'number_available',
           'review_rating', 'title', 'image_url','url_product','product_description', 'rating',])

    info_list.to_csv('resultat_catalogue.csv')


export_data_csv(doc)
