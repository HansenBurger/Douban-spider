from lib2to3.pgen2 import driver
import numpy as np
from pathlib import Path
import json, time, sys


from http.cookies import SimpleCookie

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from DecryptLogin import login
from DecryptLogin.modules.utils.cookies import saveSessionCookies

sys.path.append(str(Path.cwd() / 'Classes'))

from tools import ConfigRead
from slider_catch import do_crack



class Basic():
    def __init__(self) -> None:
        self.__exec_p = ConfigRead('drivers', 'chrome')['win_104']
        self.__option = Options()
        self.__EditOption()

    def __EditOption(self):
        # self.__option.add_argument('--headless')
        self.__option.add_argument('-disable-gpu')
        self.__option.add_argument('lang=zh_CN.UTF-8')
        # disable auto control
        self.__option.add_experimental_option('excludeSwitches', ['enable-automation'])
        

class CookiesDouban(Basic):
    def __init__(self, username:str, password:str, driver:webdriver=None):
        super().__init__()
        self.__uid = username
        self.__pwd = password
        self.__url = 'https://www.douban.com/'
        self.__driver = driver if driver else webdriver.Chrome(self._Basic__exec_p, options=self._Basic__option)
    
    def __Sleep(self, st:int=-1) -> None:
        sleep_t = st if st > 0 else np.random.rand() * 4
        time.sleep(sleep_t)

    def SaveCookie_decrypt(self):
        lg = login.Login()
        _, session = lg.douban(self.__uid, self.__pwd, 'pc')
        session.get(self.__url)
        saveSessionCookies(session=session, cookiespath='cookies.pkl')

    def SaveCookie_driver(self):
        self.__driver.get(self.__url)
        curframe = self.__driver.find_element('tag name','iframe')
        self.__driver.switch_to.frame(curframe)
        self.__Sleep()
        self.__driver.find_element('class name', 'account-tab-account').click()
        self.__driver.find_element('id', 'username').clear()
        self.__driver.find_element('id', 'username').send_keys(self.__uid)
        self.__driver.find_element('id', 'password').clear()
        self.__driver.find_element('id', 'password').send_keys(self.__pwd)
        self.__driver.find_element('xpath', '/html/body/div[1]/div[2]/div[1]/div[5]/a').click()
        self.__Sleep()

        element = self.__driver.find_element('xpath', '')
        
        self.__driver.get(self.__url)
        cookies = self.__driver.get_cookies()
        with open(ConfigRead('cookies', 'local'),'w') as cookief:
            cookief.write(json.dumps(cookies))

class CookiesLoad(Basic):
    def __init__(self, driver) -> None:
        super().__init__()
        self.__driver = driver

    def Load_driver(self):
        with open(ConfigRead('cookies','local'),'r') as cookief:
            cookies = json.load(cookief)
            for cookie in cookies:
                if isinstance(cookie.get('expiry'), float):
                    cookie['expiry'] = int(cookie['expiry'])
                    self.__driver.add_cookie(cookie)

    def Load_browser(self):
        with open(ConfigRead('cookies','tmp'),'r') as cookief:
            cookie_raw = cookief.readline()
            cookie_add = {'name':'foo','value':'bar'}
            cookie_load = SimpleCookie()
            cookie_load.load(cookie_raw)
            cookies = {k: v.value for k, v in cookie_load.items()}
            cookies.update(cookie_add)
            self.__driver.add_cookie(cookies)
    