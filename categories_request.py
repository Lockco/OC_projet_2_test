from lib2to3.pgen2 import literals
from urllib.request import Request
import requests
import pandas as pd
from bs4 import BeautifulSoup


URL = 'https://books.toscrape.com/index.html'

response = requests.get(URL)

if response.status_code != 200:
    print("le site ne répond pas")
else:
    catalogue_contents = response.text


# Création du fichier et chargument de la page dans ce fichier
with open('ArticleCatalogue.html', 'w', encoding='utf-8') as f:
    f.write(catalogue_contents)

doc = BeautifulSoup(catalogue_contents, 'html.parser')

class Request:

    def __init__(self,url = URL,doc = doc):
        print('on passe par là')
        self.url = url
        self.doc = doc

    
    def quit(self):
        print('Au revoir')
    
    
    def catch_nav_list_links(self):
        ''' Recuperation de la liste des categories, un première liste avec les titrtes et une deuxième avec les liens'''

        url = 'https://books.toscrape.com/'
        nav_list_links = doc.find('div', class_='side_categories')
        links_nav = []
        for links in nav_list_links.select('a[href]'):
            links_nav.append(url + links['href'])
           
        nav_list_title = doc.find('div', class_='side_categories')
        links_nav_title = []
        for title in nav_list_title.select('a'):
            links_nav_title.append(title.text.replace(' ',''))
            
        print(links_nav_title)

        zip_results = zip(links_nav_title, links_nav)
        final_list = list(zip_results)
        #print(final_list)
        headers_list = ['lien', 'titre']

        pd.DataFrame(final_list).to_csv('resultat.csv')
        return pd.read_csv('resultat.csv', usecols= [0])
        
    def catch_data_categories(doc):
        url = URL
        page = 1
        while page != 6:
            url = url + page
            print(url)
            page = page + 1

    #def catch_nav_list_title(self):
    def catch_book_price(doc):

        """ Recuperation du prix"""

        Book_price_tags = doc.find('p', class_='price_color')
        Book_price = []

        for tags in Book_price_tags:
            Book_price.append(tags.text.replace('Â', ''))
            print(Book_price)
        return Book_price

Request.catch_data_categories(doc)      
#Request.catch_nav_list_links(doc)
#Request.catch_nav_list_links(doc)
#Request.catch_nav_list_title(doc)