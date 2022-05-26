from bs4 import BeautifulSoup as bs
import requests
import re


def book_request(url):
    """Envoie de la requête pour récupérer le parser"""
    
    print('Etape 3 : book_request')
    response = requests.get(url)
    content_book_url = bs(response.content,'html.parser')
    return content_book_url

def catch_book_data(url):
    """Recuperation des données des livres"""

    url = book_request(url)
    print('Etape 5 catch_book_data')
    main = url.find(class_='product_main')
    book_data = {}

    book_data['title'] = main.find('h1').get_text(strip=True)
    book_data['category'] = url.find('ul', class_='breadcrumb').find_all('a')[2].get_text(strip=True)
    book_data['price'] = main.find(class_='price_color').get_text(strip=True).replace('Â', '')
    #book_data['number_available'] = main.find(class_='availability').get_text(strip=True)
    book_data['review_rating'] = ' '.join(main.find(class_='star-rating') \
                        .get('class')).replace('star-rating', '').strip()
    book_data['image_url'] = url.find(class_='thumbnail').find('img').get('src').replace('../../','https://books.toscrape.com/')
    desc = url.find(id='product_description')

    if desc:
        book_data['description'] = desc.find_next_sibling('p') \
                                .get_text(strip=True)
    book_product_table = url.find(text='Product Information').find_next('table')
    for row in book_product_table.find_all('tr'):
        header = row.find('th').get_text(strip=True)
        header = re.sub('[^a-zA-Z]+', '_', header)
        value = row.find('td').get_text(strip=True).replace('Â', '')
        book_data[header] = value
    
    return book_data

