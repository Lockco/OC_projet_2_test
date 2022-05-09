from category_request import CategoryRequest
import pandas as pd 


class Export:
    def __init__(self,title=""):
        self.title = title

def export_data(self):
        '''Export des informations au formats csv'''
        
        book_list = {'title' : CategoryRequest.catch_book_titles(self), 'price' : CategoryRequest.catch_book_price(self),'rate': CategoryRequest.catch_rating(self), 'stock' : CategoryRequest.catch_stock_availability(self), 'url' : CategoryRequest.catch_book_url(self)}

        return pd.DataFrame(book_list).to_csv('test.csv')


CategoryRequest(export_data)