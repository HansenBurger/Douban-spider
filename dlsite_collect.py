import numpy as np
import pandas as pd
from pathlib import Path
import json, time, sys

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Classes.tools import ConfigRead

home_url = r"https://www.dlsite.com"
src_url = r"/maniax/work/=/product_id/"
locales = ["ja_JP", "en_US", "zh_CN"]

driver_p = ConfigRead("drivers", "chrome")["win_106"]
option_d = Options()
option_d.add_argument("-disable-gpu")
option_d.add_argument("--silent")

def read_table(web_t:any):
    table_info = []
    table_body = web_t.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
            inds = row.find_all('th')
            cols = row.find_all('td')
            inds = [ele.text.strip() for ele in inds]
            cols = [ele.text.strip() for ele in cols]
            inds = [ele for ele in inds if ele]
            cols = [ele for ele in cols if ele]
            table_info.append(dict(zip(inds, cols)))
    return table_info


while(1):
    dl_id = input("The dlsite id: ")
    main_url = home_url + src_url + dl_id + ".html/"
    local_file = Path.cwd()/"dlsite"/(dl_id+".txt")
    with open(local_file, "w", encoding='utf-8') as f:
        f.write(dl_id)
        f.write('\n')
    for local in locales:
        loc_url = main_url +  "?locale=" + local
        driver = webdriver.Chrome(driver_p, options=option_d)
        driver.get(loc_url)
        if local != "zh_CN":
            try:
                _ = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "lang_select"))
        )
            finally:
                driver.find_element("xpath", "//a[@href='{0}']".format(loc_url)).click()
        else:
            pass
        try:
            _ = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "check_btn"))
        )
        finally:
            driver.find_element("xpath", "//a[@href='{0}']".format(src_url + dl_id + ".html/")).click()
        try:
            element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "work_right_inner"))
        )
        finally:
            loc_page = driver.page_source
            driver.close()

            loc_soup = BeautifulSoup(loc_page)
            loc_n = loc_soup.find("h1",id="work_name").contents[0]
            loc_table = loc_soup.find('table', attrs={'id':'work_outline'})
            table_i = read_table(loc_table)
            loc_maker = loc_soup.find('table', attrs={'id':'work_maker'})
            maker_i = read_table(loc_maker)

            with open(local_file, 'a', encoding='utf-8') as f:
                f.write(local)
                f.write('\n')
                f.write(loc_n)
                f.write('\n')
                for r_0 in maker_i:
                    if not r_0:
                        continue
                    r_0_i = list(r_0.keys())[0]
                    r_0_v = list(r_0.values())[0]
                    r_0_v = r_0_v.replace('\n',"\\n")
                    f.write(r_0_i+':'+r_0_v)
                    f.write('\n')
                for r_1 in table_i:
                    if not r_1:
                        continue
                    r_1_i = list(r_1.keys())[0]
                    r_1_v = list(r_1.values())[0]
                    r_1_v = r_1_v.replace('\n',"\\n")
                    f.write(r_1_i+':'+r_1_v)
                    f.write('\n')
                f.write('\n')



#RJ407323