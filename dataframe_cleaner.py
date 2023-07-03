#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import xlsxwriter


# In[2]:


#retrieve csv
folder = 'product_dataframes'
csv_name = os.listdir(folder).pop()
curr_csv = folder + '/' + csv_name


# In[3]:


#clean dataframe
products = pd.read_csv(curr_csv)
#drop and organize columns
products = products[['title', 'category', 'brand', 'price', 'mode', 'product_price_units', 'productPageUrl']]
products.rename(columns={'title':'name', 'product_price_units':'unit', 'productPageUrl':'url'}, inplace=True)


# In[4]:


#update urls
products['url'] = 'https://centralsquare.dailytable.org' + products['url']


# In[5]:


#remove incorrect items (items with price 999 are faulty)
products = products.drop(products[products['price'] == 999.00].index)


# In[6]:


#correct brands
brands = {brand.replace('\n', '') for brand in open('brands.txt', 'r').readlines()}
for brand in brands:
    products.loc[products['name'].str.contains(brand), 'brand'] = brand
    products['name'] = products['name'].map(lambda x: x.replace(brand, ''))


# In[7]:


#shorten excessive category names
products.loc[products['category'] == 'Canned Beans, Fruits & Vegetables', 'category'] = 'Canned Beans, Fruit & Veg'
products.loc[products['category'] == 'Salad Dressings, Sauces & Condiments', 'category'] = 'Dressings, Sauces & Condiments'


# In[8]:


#sort and export to cleaned folder
products = products.sort_values(by=['category'])
products.to_csv(folder + '_cleaned/' + csv_name, index=False)


# In[ ]:




