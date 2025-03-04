import itertools
import random
import selenium
from selenium.webdriver import ActionChains
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os,time
from newspaper import Article
import pandas as pd

def extract_text(url):
    '''
    description : The function to extract only main text from article
    :param url: url of the article
    :return: text of article
    '''
    article = Article(url)
    article.download()
    article.parse()
    text = article.text or 'N/A' #text가 없는 경우 'N/A'로 출력
    return text

try:
    ### webdriver options
    options = Options()
    options.add_experimental_option('detach',True)
    options.add_argument('--lang=en-US') # set region as US
    # ====== 🔔 크롬에서 "권한허용" 확인창이 뜨는 경우 🔔 ======
    # 웹드라이버 생성 시 options키워드 인수로 추가옵션을 설정해야 한다.
    # 크롬의 경우 1이 허용, 2가 차단
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
    # ======================================================
    # options.add_argument('--headless=new')

    driver = webdriver.Chrome(
        options=options
    )

    # resize the window size
    driver.set_window_size(width=1280 , height=1024)

    # request initial url
    url = 'https://google.com'
    driver.get(url)
except Exception as e :
    print(e)