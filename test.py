from encodings import utf_8
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd



URL = 'https://books.toscrape.com/'
response = requests.get(URL)
doc = bs(response.text,'html.parser')

def title():
    """Recuperation des titres"""

    Book_title = content_catalog.find_all('h1')
    Book_titles = []

    for title in Book_title:
        Book_titles.append(title.text)
    print(Book_titles)
    return Book_titles

def rate():
    
    rating_list= []
    for rate in content_catalog.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        rating_list.append(rate.select("p:nth-of-type(1)")[0].get('class')[1])
    print(rating_list)
    return rating_list

def catch_book_price():
    """ Recuperation du prix"""

    book_price = []
    book_price_tags = content_cat.find_all('p', class_='price_color')
    
    for tags in book_price_tags:
        book_price.append(tags.text.replace('Â', ''))
    return book_price

def catch_stock_availability():
        """ Recuperation de la disponibilite """

        book_stock = []
        book_stock_tags = content_cat.find_all('p', class_ = 'instock availability')
        
        for tags in book_stock_tags:
            book_stock.append(tags.text.strip())
        return book_stock

def catch_book_url():
        """ Recuperation des urls"""
        links = []

        for link in doc.findAll('article', class_ = 'product_pod'):
            url = link.find('a', href=True).get('href')
            books_url =( URL + url)
            links.append(books_url)
        
        return links
                
        # book_url_tags = content_cat.find('ol', class_='row')
        # book_url = []

        # for link in book_url_tags.select('a[href]'):
        #     book_url.append(url + link['href'].replace('../../../',''))
            
        # delete_duplicate =[]
        # for i in book_url:
        #     if i not in delete_duplicate:
        #         delete_duplicate.append(i)
        # return delete_duplicate

nav_list_links = doc.find('div', class_='side_categories')
links_nav = [link['href'] for link in nav_list_links.select('a[href]')]

nav_list = []
nav = (len(links_nav))

j = 0
print('on entre')
for link in links_nav:
    result = requests.get('https://books.toscrape.com/catalogue/' + link)
    content = result.text
    content_cat = bs(content, 'lxml')
    print('Extraction da la categorie : ', link)

    for i in range(nav):
        print('catégorie: ',[i])
        nav_list.append(link)
        #title()        
        # rate()
        # catch_book_price()
        # catch_stock_availability() 
        catalog = catch_book_url()
        
    for a in catalog:
        #print('Extraction de la page : ',[a])
        #print('extraction catalogue : ',a )
        result_url = requests.get(a)
        url_catalog = result_url.text
        content_catalog = bs(url_catalog,'lxml')
        title()
        print(title)
        #rate()
                
        books_data = {'titre':title()}
        df = pd.DataFrame(books_data).to_csv('category'+str(j)+'.csv', encoding = 'utf-8')
    j += 1