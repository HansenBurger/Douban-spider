import numpy as np
import pandas as pd
import sys, time, json
from pathlib import Path

from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

sys.path.append(str(Path.cwd() / 'Classes'))

from tools import ConfigRead
from cookies import CookiesLoad


options = Options()
options.add_argument('--headless')

class SpiderBasic():
    def __init__(self) -> None:
        self.__wait_st = 10
        self.__exec_p = ConfigRead('drivers', 'chrome')['win_104']
        self.__option = Options()
        # self.__option.add_argument('--headless')

    def __RandSleep(self) -> None:
        time.sleep(np.random.rand() * 4)


class SpiderTags(SpiderBasic):
    def __init__(self,header:dict) -> None:
        super().__init__()
        self.__url = r'https://book.douban.com/'

class SpiderSearch(SpiderBasic):
    def __init__(self) -> None:
        super().__init__()
        self.__driver = webdriver.Chrome(self._SpiderBasic__exec_p, options=self._SpiderBasic__option)
        self.__url = r'https://search.douban.com/book/subject_search'

    def __AddCookies(self):
        self.__driver.delete_all_cookies()
        CookiesLoad(self.__driver).Load_driver()

    def __ContentDetect(self, li: any, find_c: str, find_n: str):
        try:
            content = li.find(find_c, {'class', find_n}).contents[0]
        except:
            content = None
        return content

    def QuoteByTexts(self, text_s: list, try_st:int=20):
        page_n = 0
        self.__AddCookies()
        df_book_s = []
        for text_ in text_s:
            book_i_s = []
            while(try_st):
                url = self.__url + '/?search_text='+urllib.parse.quote(
                text_) +'&cat=1001'+ '&start=' + str(page_n * 15)
                self.__driver.get(url)
                html = self.__driver.page_source
                soup = BeautifulSoup(html)
                book_page_all = soup.find_all('div', {'class':'detail'})

                if not book_page_all:
                    try_st -= 1
            
                for book_i in book_page_all:
                    book_i_d = {}
                    book_i_d['url'] = book_i.find('a', href=True)['href']
                    book_i_d['star'] = self.__ContentDetect(book_i, 'span', 'rating_nums')
                    book_i_d['public'] = self.__ContentDetect(book_i, 'span', 'pl')
                    book_i_d['abstract'] = self.__ContentDetect(book_i, 'div', 'meta abstract')
                    book_i_s.append(book_i_d)

                page_n += 1
                print('Collected Book Info From Page {0}'.format(page_n))
                try:
                    df_book_i = pd.DataFrame(book_i_s)
                except:
                    df_book_i = pd.DataFrame()
                self.__driver.close()
            df_book_s.append(df_book_i)
        return df_book_i