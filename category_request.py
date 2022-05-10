import requests
import pandas as pd
from bs4 import BeautifulSoup as bs





    
URL = 'https://books.toscrape.com/catalogue/category/books/fiction_10/'

response = requests.get(URL)
doc = bs(response.text,'html.parser')

class CategoryRequest:

    def __init__(self,url = URL,doc =doc,nav_list_links=[],book_titles=[],rating=[],book_price=[],stock_availability=[],book_url=[],data_page=[],data_pages=[]):
        print('on passe par là')
        self.url = url
        self.doc = doc
        self.nav_list_links = nav_list_links
        self._book_titles = book_titles
        self.rating = rating
        self.book_price = book_price
        self.stock_availability = stock_availability
        self.book_url= book_url
        self.data_page = data_page
        self.data_pages = data_pages
        


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

        headers_list = {'tirtre': links_nav_title , 'liens': links_nav}

        pd.DataFrame(headers_list).to_csv('list-categories.csv')
        pd.read_csv('resultat.csv', usecols= [0])
        return self.nav_list_links

    def catch_book_titles(self):
        """Recuperation des tires"""

        book_title = doc.find_all('h3')
        book_titles = []
        for title in book_title:
            book_titles.append(title.text)
        print (len(book_titles))
        return book_titles

    def catch_rating(self):
        """ Recuperation des notes """
        rating_book = doc.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        rating_list= []
        star = doc
        for star in rating_book:
            rating_list.append(star.select("p:nth-of-type(1)")[0].get('class')[1])
        print(len(rating_list))
        return rating_list

    def catch_book_price(self):
        """ Recuperation du prix"""

        book_price_tags = doc.find_all('p', class_='price_color')
        book_price = []
        
        for tags in book_price_tags:
            book_price.append(tags.text.replace('Â', ''))
        print(len(book_price))
        return book_price

    def catch_stock_availability(self):
        """ Recuperation de la disponibilite """
        book_stock_tags = doc.find_all('p', class_ = 'instock availability')
        book_stock = []

        for tags in book_stock_tags:
            book_stock.append(tags.text.strip())
        print(len(book_stock))
        return book_stock
    
    def catch_book_url(self):
        """ Recuperation des urls"""
        
        url = 'https://books.toscrape.com/catalogue/'
        book_url_tags = doc.find('ol', class_='row')
        book_url = []

        for link in book_url_tags.select('a[href]'):
            book_url.append(url + link['href'].replace('../../../',''))
     
        delete_duplicate =[]
        for i in book_url:
            if i not in delete_duplicate:
                delete_duplicate.append(i)

        return delete_duplicate

    def catch_data_pages(self):
        """Export des informations au formats csv"""
        
        book_list = {'title' : CategoryRequest.catch_book_titles(self), 'price' : CategoryRequest.catch_book_price(self),'rate': CategoryRequest.catch_rating(self), 'stock' : CategoryRequest.catch_stock_availability(self), 'url' : CategoryRequest.catch_book_url(self)}

        pd.DataFrame(book_list).to_csv('test.csv')
        return self.data_page