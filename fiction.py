import numpy as np
import pandas as pd
from pathlib import Path
import json, time, sys

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from Classes.tools import ConfigRead

src_url = 'https://www.cool18.com/bbs4/index.php?app=forum&act=threadview&tid=14241451'
driver_p = ConfigRead('drivers', 'chrome')['win_106']
option_d = Options()
option_d.add_argument('-disable-gpu')
driver = webdriver.Chrome(driver_p, options=option_d)
driver.get(src_url)

src_page = driver.page_source
src_soup = BeautifulSoup(src_page)

parag_tot = []
paper_main = src_soup.find("pre").contents
a = 1