from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re
from os.path  import basename
#from urllib.parse import urljoin


URL = 'https://books.toscrape.com/'
get_url = requests.get(URL)
content = bs(get_url.text, 'html.parser')

def catch_book_url():
        """ Recuperation des urls de chaque livre"""
        
        book_url = []
        book_url_tags = content_cat.find('ol', class_='row')

        for link in book_url_tags.select('a[href]'):
            links = (URL +'catalogue/'+ link['href'].replace('../../../',''))
            if links not in book_url:
                book_url.append(links)
        
        return book_url

def catch_book_data():
    """Recuperation des données des livres"""

    main = content_book_url.find(class_='product_main')
    book_data = {}

    book_data['title'] = main.find('h1').get_text(strip=True)
    # book_data['category'] = main.find('ul', class_='breadcrumb')\
    #                         .find_all('a')[0].get_text(strip=True)
    book_data['price'] = main.find(class_='price_color').get_text(strip=True).replace('Â', '')
    book_data['number_available'] = main.find(class_='availability').get_text(strip=True)
    book_data['review_rating'] = ' '.join(main.find(class_='star-rating') \
                        .get('class')).replace('star-rating', '').strip()
    book_data['img'] = content_book_url.find(class_='thumbnail').find('img').get('src').replace('../../','https://books.toscrape.com/')
    desc = content_book_url.find(id='product_description')
    book_data['product_description'] = ''

    if desc:
        book_data['description'] = desc.find_next_sibling('p') \
                                .get_text(strip=True)
    book_product_table = content_book_url.find(text='Product Information').find_next('table')
    for row in book_product_table.find_all('tr'):
        header = row.find('th').get_text(strip=True)
        header = re.sub('[^a-zA-Z]+', '_', header)
        value = row.find('td').get_text(strip=True).replace('Â', '')
        book_data[header] = value

    return book_data

def catch_categories_url():
    """ Recuperation des urls de chaque categories"""

    categories = content.find('ul', {'class': 'nav nav-list'}).find('li').find('ul').find_all('li')
    categories_url= []

    for category in categories: 

        category_name = category.find('a').text.strip()
        category_url_relative = category.find('a').get('href')
        category_url = URL + category_url_relative
        categories_url.append(category_url)
        
    return categories_url

# category_book = content.find('ul', class_='breadcrumb').find_all('a')[2].get_text(strip=True)
# #category = category_book.find_all('a')[2].get_text(strip=True)
# print(category_book)

def catch_images():
    """ Recuperation des images"""

    images = content.find_all('img')

    for item in images:
        url_images =(URL + item['src'])
        print(url_images)
        with open(basename(url_images), 'wb') as f:
            f.write(requests.get(url_images).content)

j = 0
for link in catch_categories_url():
   
    print('extraction de la category : ', link)
    result = requests.get(link)
    content = result.text
    content_cat = bs(content, 'lxml')

    list_books = []
    for url in catch_book_url():

        print('extraction de la page : ', url)
        result_book_url = requests.get(url)
        content = result_book_url.text
        content_book_url = bs(content, 'lxml')
        book = catch_book_data()
        list_books.append(book)
        print('Sauvegarde',book)
    df = pd.DataFrame.from_dict(list_books).to_csv('categories' + str(j) + '.csv', encoding = 'utf-8')
    j += 1



