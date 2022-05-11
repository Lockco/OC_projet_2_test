from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/catalogue/page-1.html'
response = requests.get(url)
doc = bs(response.text,'html.parser')

def title():

    liste_titles = []
    for titles in content_cat.find_all('h3'):
        liste_titles.append(titles.get_text())


def rate():
    rating_list= []
    for rate in content_cat.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        rating_list.append(rate.select("p:nth-of-type(1)")[0].get('class')[1])

def catch_book_price():
    """ Recuperation du prix"""

    book_price = []
    book_price_tags = content_cat.find_all('p', class_='price_color')
    
    for tags in book_price_tags:
        book_price.append(tags.text.replace('Â', ''))
        
def catch_stock_availability():
        """ Recuperation de la disponibilite """

        book_stock = []
        book_stock_tags = content_cat.find_all('p', class_ = 'instock availability')
        
        for tags in book_stock_tags:
            book_stock.append(tags.text.strip())
            print (book_stock)

def catch_book_url():
        """ Recuperation des urls"""
        
        url = 'https://books.toscrape.com/catalogue/'
        book_url_tags = content_cat.find('ol', class_='row')
        book_url = []

        for link in book_url_tags.select('a[href]'):
            book_url.append(url + link['href'].replace('../../../',''))
            
        delete_duplicate =[]
        for i in book_url:
            if i not in delete_duplicate:
                delete_duplicate.append(i)
            print(delete_duplicate)

nav_list_links = doc.find('div', class_='side_categories')
links_nav = [link['href'] for link in nav_list_links.select('a[href]')]

for link in links_nav:
    result = requests.get('https://books.toscrape.com/catalogue/' + link)
    content = result.text
    content_cat = BeautifulSoup(content, 'lxml')

    title()        
    rate()
    catch_book_price()
    catch_stock_availability() 
    catch_book_url()