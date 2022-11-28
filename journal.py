import numpy as np
import pandas as pd
from pathlib import Path
import json, time, sys

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from Classes.tools import ConfigRead

#src_url = 'https://www.sciencedirect.com/journal/computers-in-biology-and-medicine/vol/149/suppl/C'
src_url = 'https://www.sciencedirect.com/journal/computer-methods-and-programs-in-biomedicine/vol/225/suppl/C'
driver_p = ConfigRead('drivers', 'chrome')['win_104']
option_d = Options()
option_d.add_argument('-disable-gpu')
driver = webdriver.Chrome(driver_p, options=option_d)
driver.get(src_url)

src_page = driver.page_source
src_soup = BeautifulSoup(src_page)
article_tot = []
article_ch_s = src_soup.find_all('ol', {'class', 'article-list'})
for chapter in article_ch_s:
    article_s = chapter.find_all('a', {'class', 'anchor article-content-title u-margin-xs-top u-margin-s-bottom anchor-default'})
    article_tot.extend(article_s)

art_time_d_l = []

for article in article_tot:
    a_p_url = article.attrs['href']
    a_t_url = 'https://www.sciencedirect.com' + a_p_url
    driver.get(a_t_url)
    while(1):
        time.sleep(np.random.rand()*4)
        button = driver.find_element('id', 'show-more-btn')
        if not button:
            continue
        else:
            break
    button.click()
    a_i_page = driver.page_source
    a_i_soup = BeautifulSoup(a_i_page)
    art_info = a_i_soup.find('div',{'class', 'wrapper'})
    art_time = art_info.find('p').get_text()
    l = art_time.split(', ')
    try:
        art_time_d = {
        'Received': art_time.split(', ')[0].split('Received ')[1],
        'Revised': art_time.split(', ')[1].split('Revised ')[1],
        'Accepted': art_time.split(', ')[2].split('Accepted ')[1],
        'AvailableOnline': art_time.split(', ')[3].split('Available online ')[1]
    }
    except:
        continue
    art_time_d_l.append(art_time_d)
    time.sleep(np.random.rand()*4)

df = pd.DataFrame(art_time_d_l)
df.to_csv('CMPB.csv', index=False)
