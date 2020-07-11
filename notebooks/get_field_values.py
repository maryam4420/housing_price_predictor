#!/usr/bin/env python
# coding: utf-8

# In[4]:


from bs4 import BeautifulSoup
import requests


# In[21]:


from bs4 import BeautifulSoup
import requests
import time, os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# from re import sub
# from decimal import Decimal

# In[298]:


myfile = "page_source2265"
with open(myfile, "r") as file:
    page = file.read()
soup = BeautifulSoup(page,'lxml')
outp = soup.find('div', {'class':'Grid__GridContainer-sc-5ig2n4-1 eVbKXM'})

# info at the top: price, # of bed & bath, sqft etc.
price = soup.find('div', {'class':'Text__TextBase-sc-1i9uasc-0-div Text__TextContainerBase-sc-1i9uasc-1 qAaUO'}).text
bed = soup.find_all('li', {'data-testid':'bed'})[1].text
bath = soup.find_all('li', {'data-testid':'bath'})[1].text
sqft = soup.find_all('li', {'data-testid':'floor'})[1].text
area = outp.find('a').text
zipcode = outp.find_all('span')[1].text
address = outp.find_all('span')[0].text
date_sold = soup.find('div', {'class':'Text__TextBase-sc-1i9uasc-0-div Text__TextContainerBase-sc-1i9uasc-1 cERLyX'}).text


# info in the bottom: home_type, sqft, lot_size, year_built

outp2 = soup.find('section', {'id': 'main-content'})
home_detail_summ = outp2.find('div', {'data-testid': 'home-details-summary-container'})
features_detail = outp2.find('ul',{'data-testid': 'home-features'})
features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})

home_type = features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})[0].text
sqft_price = features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})[1].text
lot_size = features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})[2].text
year_built = features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})[3].text
year_or_hoafee = features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})[4].text

# get tax, and text
tax = soup.find(text='Tax').findNext().text
disc = soup.find('div', {'data-testid':'home-description-text-description-sub-header'}).text
text = soup.find('div', {'data-testid':'home-description-text-description-text'}).text



price, bed,bath,sqft, area,zipcode,address, date_sold, home_type, sqft_price, lot_size, year_built, year_or_hoafee, tax, disc,  text



# In[236]:


myfile = "page_source32"
with open(myfile, "r") as file:
    page = file.read()
soup = BeautifulSoup(page,'lxml')
outp = soup.find('div', {'class':'Grid__GridContainer-sc-5ig2n4-1 eVbKXM'})

# info at the top: price, # of bed & bath, sqft etc.
price = soup.find('div', {'class':'Text__TextBase-sc-1i9uasc-0-div Text__TextContainerBase-sc-1i9uasc-1 qAaUO'}).text
price = int(price.strip('$').replace(',',''))

bed = soup.find_all('li', {'data-testid':'bed'})[1].text
bed = int(bed.split(" ")[0])

bath = soup.find_all('li', {'data-testid':'bath'})[1].text
bath = int(bath.split(" ")[0])

sqft = soup.find_all('li', {'data-testid':'floor'})[1].text
sqft = sqft.split(" ")[0] 
sqft = int(sqft.strip('$').replace(',',''))

area = outp.find('a').text

zipcode = outp.find_all('span')[1].text
zipcode = (zipcode.split(',')[1]).split(' ')[2]
zipcode = int(zipcode.strip('$').replace(',',''))

address = outp.find_all('span')[0].text

date_sold = soup.find('div', {'class':'Text__TextBase-sc-1i9uasc-0-div Text__TextContainerBase-sc-1i9uasc-1 cERLyX'}).text
date_sold = date_sold.split(':')[1]
date_sold = datetime.strptime(date_sold.strip(), '%b %d, %Y')

# info in the bottom: home_type, sqft, lot_size, year_built

outp2 = soup.find('section', {'id': 'main-content'})
home_detail_summ = outp2.find('div', {'data-testid': 'home-details-summary-container'})
features_detail = outp2.find('ul',{'data-testid': 'home-features'})
features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})

home_type = features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})[0].text

sqft_price = features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})[1].text
sqft_price = int((sqft_price.strip('$')).split('/')[0])

lot_size = features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})[2].text
lot_size = ((((lot_size.strip())).split(':')[1]).strip()).split(' ')[0]
lot_size = int(lot_size.replace(',',''))



year_built = features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})[3].text
year_or_hoafee = features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})[4].text

price, bed,bath,sqft, area,zipcode,address, date_sold, home_type, sqft_price, lot_size, year_built, year_or_hoafee


# In[208]:


int(lot_size)


# In[ ]:


datetime.strptime('6-Mar-2016', '%d-%b-%Y').strftime('%Y-%m-%d')

Jun 30, 2020


# In[225]:


from datetime import datetime


# In[230]:


d = datetime.strptime('Jun 30, 2020', '%b %d, %Y').strftime("%d/%m/%Y")


# In[231]:


type(d)


# In[234]:


d = datetime.strptime(date_sold.strip(), '%b %d, %Y')


# In[235]:


d


# In[299]:


pwd


# In[ ]:




