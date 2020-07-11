#!/usr/bin/env python
# coding: utf-8

# In[7]:


get_ipython().system('echo $PATH')


# In[8]:


from bs4 import BeautifulSoup
import requests
import time, os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import pickle  # https://wiki.python.org/moin/UsingPickle


# In[9]:


from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

binary = FirefoxBinary('/usr/bin/firefox')
browser = webdriver.Firefox(firefox_binary=binary)


# In[10]:


driver = webdriver.Firefox()


# In[12]:


driver.get('https://www.trulia.com/sold/Seattle,WA/')


# soup = BeautifulSoup(driver.page_source, 'html.parser')

# len(driver.page_source)

# Repeat the steps above to create the a list containing the link from all the pages:

# In[46]:


# master_list = []
# for i in range (1, 280):
#     url = 'https://www.trulia.com/sold/Seattle,WA/' + str(i) + '_p'
#     driver.get(url)
#     time.sleep(15)
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     master_list.extend([link.get('href') for link in soup.find('div', id = 'resultsColumn').find_all('a')][:30])
#     if i%10 == 0:
#         with open('Trulia_housing_data.pkl', 'wb') as picklefile:
#             pickle.dump(master_list,picklefile)


# In[133]:


# len(master_list)


# In[143]:


# with open('Trulia_housing_dataArash.pkl', 'wb') as picklefile:
#             pickle.dump(master_list,picklefile)


# In[13]:


target = "Trulia_housing_dataArash.pkl"
if os.path.getsize(target) > 0:      
    with open(target, "rb") as f:
        unpickler = pickle.Unpickler(f)
        # if file is not empty scores will be equal
        # to the value unpickled
        master_list = unpickler.load()


# In[109]:


# from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
# req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
# proxies = req_proxy.get_proxy_list() #this will create proxy list


# In[110]:


# us_proxies = [] #int is list of Indian proxy
# for proxy in proxies:
#     if proxy.country == 'United States':
#         us_proxies.append(proxy)
        
# print(us_proxies)


# In[111]:


# PROXY = us_proxies[5].get_address()
# webdriver.DesiredCapabilities.CHROME['proxy']={
#     "httpProxy":PROXY,
    
#     "proxyType":"MANUAL",
    
# }


# In[16]:


import subprocess
os.system("expressvpn disconnect")
os.system("expressvpn connect 'United States'")
os.system("echo '!curl https://ipinfo.io/ip'")


# In[26]:


time.sleep(10)


# In[34]:


i


# In[ ]:


options = webdriver.FirefoxOptions()
options.add_argument('-headless')

driver = webdriver.Firefox()

i = 7959
while i<9000:
    link = master_list[i]
    i += 1
    if i%10 == 0:
        print(f"processing ./page_sources/page_source{i}+ ...")
    
    driver.get('https://www.trulia.com' + link)

    page_text = driver.page_source
    
    if "<title>Access to this page has been denied.</title>" in page_text:
        print(f"./page_sources/page_source{i} didn't load because of access denied." )
        os.system("expressvpn disconnect")
        os.system("expressvpn connect 'United States'")
        print(".... Switched IP Address ....")
        
        driver.close()
        driver = webdriver.Firefox()

        i -= 1
        time.sleep(30)
    
    with open(f"./page_sources/page_source{i}", "w") as f:
        f.write(page_text)
driver.close()


# In[78]:


import os
os.getcwd()


# houses = ''
# for link in master_list[1:5]:
#     driver = webdriver.Chrome(chromedriver)
#     driver.get('https://www.trulia.com' + link)
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     for jump, facts in strings:
#         try:
#             houses.append(get_details(soup, jump, facts))
#             break
#         except:
#             continue
#     driver.quit()
#     time.sleep(1)

# In[ ]:


myfile = "page_source1870"
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
home_type = features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})[0].text
sqft_price = features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})[1].text
lot_size = features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})[2].text
year_built = features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})[3].text
year_or_hoafee = features_detail.find_all('li', {'class':'FeatureList__FeatureListItem-iipbki-0 fKDDGQ'})[4].text

price, bed,bath,sqft, area,zipcode,address, date_sold, home_type, sqft_price, lot_size, year_built, year_or_hoafee

