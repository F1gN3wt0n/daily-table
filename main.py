from bs4 import BeautifulSoup
import requests as re
from selenium import webdriver
from nutritionix import Nutritionix
from Product import Product

NIX = Nutritionix(app_id="4fc0e6d1", api_key="f5aa485183f8a423a0a6465f463aa77c")

def get_sub_links(scraper_link, preface_link, selector):
    #grab all 'a' attributes (where links stored) from page
    html = re.get(scraper_link).text
    indexer = BeautifulSoup(html, 'html.parser')
    a_tagged = indexer.find_all('a')

    sub_links = set()
    for a in a_tagged:
        sub_link = a.get('href') #retrieve link attribute
        if sub_link is not None and selector in sub_link:
            sub_links.add(preface_link+sub_link)
    return sub_links

def get_product_codes(category_link):
    #will only work with Chrome installed
    driver = webdriver.Chrome()
    driver.get(category_link)
    source = driver.page_source
    print(source)

def get_nutrition(products, isle):
    for product in products:
        try:
            if isle in ['Fresh Vegetables', 'Fresh Fruits'] and 'Little Leaf Farms' not in product.get_name():
                info = NIX.item(id=NIX.search(product.get_name() + ' raw', brand_id='513fcc648110a4cafb90ca5e').json()['hits'][0]['_id']).json()
            else:
                info = NIX.item(id=NIX.search(product.get_name()).json()['hits'][0]['_id']).json()

            product.set_nutrition_unit(info['nf_servings_per_container'],
                                        info['nf_serving_size_qty'],
                                        info['nf_serving_size_unit'],
                                        info['nf_serving_weight_grams'])
            product.set_nutrition(info['nf_calories'],
                                    info['nf_calories_from_fat'],
                                    info['nf_total_fat'],
                                  info['nf_saturated_fat'],
                                  info['nf_trans_fatty_acid'],
                                  info['nf_polyunsaturated_fat'],
                                  info['nf_monounsaturated_fat'],
                                  info['nf_cholesterol'],
                                  info['nf_sodium'],
                                  info['nf_total_carbohydrate'],
                                  info['nf_dietary_fiber'],
                                  info['nf_sugars'],
                                  info['nf_protein'],
                                  info['nf_vitamin_a_dv'],
                                  info['nf_vitamin_c_dv'],
                                  info['nf_calcium_dv'],
                                  info['nf_iron_dv'])
            #print(product.get_name(), product.get_nutritional_unit())
        except:
            print('ERROR')
            print(product.get_name(), NIX.search(product.get_name()).json())

def get_spreadsheet(products):
    for isle in products.keys():
        if isle not in ['Paper Plastic Products', 'Cleaning Products']:
            get_nutrition(products[isle], isle)

if __name__ == '__main__':
    #getting all product links
    store = 'https://centralsquare.dailytable.org' #change this to look at different stores
    departments = get_sub_links(store, store, '/department/')
    categories = set()
    for department in departments:
        categories |= get_sub_links(department, store, 'category')
    product_codes = set()
    for category_link in categories:
        product_codes |= get_product_codes(category_link)
    print(product_codes)
