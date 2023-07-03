from bs4 import BeautifulSoup
import requests
import re
import json
import pandas as pd
import datetime

def get_sublinks(scraper_link, preface_link, selector):
    """
    takes:
        scrapper_link: a link pointing to the webpage to be scrapped
        preface_link: the beginning of the links to be generated
        selector: a string that must be present in links scrapped from scrapper_link
    returns:
        sublinks: a set of sublinks containing 'selector' with the preface_link front-added
    """
    sublinks = set()
    html = requests.get(scraper_link).text
    indexer = BeautifulSoup(html, 'html.parser')
    a_tagged = indexer.find_all('a')
    for a in a_tagged:
        sublink = a.get('href') #retrieve link attribute
        if sublink is not None and selector in sublink:
            #ignore some product categories
            if all(cat not in sublink for cat in {'prepared', 'beverages', 'household'}):
                sublinks.add(preface_link+sublink)
    return sublinks

def get_products(category_link, num_pages):
    """
    takes:
        category_link: link to the category being scrapped
        num_pages: number of pages present in the category
    returns:
        products: a pandas dataframe. Rows are each product in the category
    """
    products = pd.DataFrame()
    #interate over each page in the category
    for curr_page in range(1, num_pages+1):
        url = category_link+'?page='+str(curr_page)+'&per-page=24'
        html = requests.get(url).text
        #retrieve the product cards from page
        product_cards = re.findall(r'var ProductCard\S+_props = (.*);', html)
        for product in product_cards:
            product = re.sub(r'"[^"]+":ProductCard[^,\s]+,?', '', product) #remove preface
            product_json = json.loads(product) #turn str into json
            product_df = pd.DataFrame([product_json]) #turn into dataframe
            products = pd.concat([products, product_df])
    return products

if __name__ == '__main__':
    #retrieve departments
    store = 'https://centralsquare.dailytable.org' #change this to look at different stores
    departments = get_sublinks(store, store, '/department/')
    #retrieve categories
    categories = set()
    for department in departments:
        categories |= get_sublinks(department, store, 'category')
    #products to dataframe
    products = pd.DataFrame()
    for category_link in categories:
        num_pages = max(len(get_sublinks(category_link, category_link, 'page=')), 1)
        products = pd.concat([products, get_products(category_link, num_pages)])
    #save to csv
    products = products.reset_index(drop=True)
    date = datetime.datetime.now()
    date = date.strftime('%m_%d_%Y')
    products.to_csv('product_dataframes/'+date+'.csv')
