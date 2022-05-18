from sys import flags
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re
from os.path  import basename
from urllib.parse import urljoin

URL = 'https://books.toscrape.com/'
get_url = requests.get(URL)
CONTENT = bs(get_url.text, 'html.parser')

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
    book_data['category'] = content_book_url.find('ul', class_='breadcrumb').find_all('a')[2].get_text(strip=True)
    book_data['price'] = main.find(class_='price_color').get_text(strip=True).replace('Â', '')
    book_data['number_available'] = main.find(class_='availability').get_text(strip=True)
    book_data['review_rating'] = ' '.join(main.find(class_='star-rating') \
                        .get('class')).replace('star-rating', '').strip()
    book_data['img'] = content_book_url.find(class_='thumbnail').find('img').get('src').replace('../../','https://books.toscrape.com/')
    desc = content_book_url.find(id='product_description')

    if desc:
        book_data['description'] = desc.find_next_sibling('p') \
                                .get_text(strip=True)
    book_product_table = content_book_url.find(text='Product Information').find_next('table')
    for row in book_product_table.find_all('tr'):
        header = row.find('th').get_text(strip=True)
        header = re.sub('[^a-zA-Z]+', '_', header)
        value = row.find('td').get_text(strip=True).replace('Â', '')
        book_data[header] = value
    print(book_data)
    return book_data

def catch_categories_url():
    """ Recuperation des urls de chaque categories"""

    categories = CONTENT.find('ul', {'class': 'nav nav-list'}).find('li').find('ul').find_all('li')
    categories_url= []
    categories_name = []
    for category in categories: 

        category_name = category.find('a').text.strip()
        flag = 1
        while True:
            
            category_url_relative = category.find('a').get('href').replace('index.html', f"page-{flag}.html")
            flag +=1
            category_url = URL + category_url_relative
            response = requests.get(category_url)
            if response.status_code == 200:
                categories_url.append(category_url)
                categories_name.append(category_name)
            else:
                break
    
    return categories_url

def catch_images():
    """ Recuperation des images"""

    images = CONTENT.find_all('img')
    a,b = catch_categories_url()
    for image in images:
        name = image['alt']
        link =(URL + image['src'])
        print(link)
        with open((f"data\images\{name}.jpg").replace(' ','').replace(':', ''), 'wb') as f:
            f.write(requests.get(link).content)

def catch_all_url():
    
    page_url = []
    for link in catch_categories_url():
        while True:
            print('extraction de la category : ', link)
            result = requests.get(link)
            content = result.text
            content_cat = bs(content, 'lxml')
            
            next_page_element = content_cat.select_one('li.next > a')
            if next_page_element:
                next_page_url = next_page_element.get('href')
                link = urljoin(link, next_page_url)

            else:
                break
            page_url.append(link)
    print(page_url)


print('on entre')
j = 0
categ_url = catch_categories_url

for link in categ_url:
    print('on entre')
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
    with open(("data\images\categorie.csv").replace(' ','').replace(':', ''), 'wb') as f:
            f.write(requests.get(link).content)
    j += 1


