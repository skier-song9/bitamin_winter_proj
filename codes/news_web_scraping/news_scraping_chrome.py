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

def parse_date_format(date_str):
    '''
    description : parse google news date format to pandas datetime(yyyy-mm-dd)
    :param date_str: Month Day Year format or '1d ago', '1week ago', ...
    :return: 'yyyy-mm-dd' format string
    '''
    month_dict = {'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5',
             'Jun':'6','Jul':'7','Aug':'8','Sep':'9','Oct':'10',
             'Nov':'11','Dec':'12'}
    m,d,y = date_str.split()
    if y == 'ago':
        y = 2023
        if m == '4': d=4;
        elif m == '3' : d=11;
        elif m == '2' : d=18;
        elif m == '1' : d=25;
        else : d=30;
        m = 12
        pass
    else:
        m = month_dict[m]
        d = d[:-1]
    return f'{y}-{m}-{d}'

def netflix_news_scraping_s2e(year, month):
    '''
    description : scrap news from start_date to 3 month after. start_date = year-month
        e.g.) year=2019, month=[1,2,3] -> scraping from 2019-01-01 ~ 2019-04-01
    :param year: integer
    :param month: list of 3 month for crawling
    :return: dataframe composed of url, title, date columns.
    '''
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

        ### Search Netflix on google
        # wait until google home is loaded & find wearch engine
        google_search = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="APjFqb"]')))
        # click search engine and send 'Netflix' keyword
        google_search.click()
        google_search.send_keys('Netflix')
        google_search.send_keys(Keys.ENTER) # search

        '''
        initialize variables
        '''
        articles_url, articles_title, articles_date = [], [], []

        # Click 'change to English'
        try:
            change_to_en = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="Rzn5id"]/div/a[2]')))
            change_to_en.click()
        except (TimeoutException,NoSuchElementException) as c2e_e:
            print("change_to_english 없음.")

        ### click news tab
        try:
            netflix_news_tab = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="bqHHPb"]/div/div/div[1]/a[2]/div')))
            netflix_news_tab.click()
        except (TimeoutException,NoSuchElementException) as netflix_news_tab_e:
            try:
                every_filter_btn = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="uddia_1"]/span/g-popup/div[1]/div')))
                every_filter_btn.click()
                netflix_news_tab = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="_Y7GyZbaKDZKb2roPiJ-P8AY_21"]/g-menu/g-menu-item[5]/div/a')))
            except Exception as EEE:
                try:
                    netflix_news_tab = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="hdtb-msb"]/div[1]/div/div[2]/a')))
                    netflix_news_tab.click()
                except Exception as eee:
                    try:
                        netflix_news_tab = driver.find_element(By.CSS_SELECTOR,'#hdtb-sc > div > div > div.zp6Lyf.FpfXM > div.IUOThf > a:nth-child(2)')
                        netflix_news_tab.click()
                    except Exception as eeee:
                        netflix_news_tab = driver.find_element(By.XPATH,'// *[ @ id = "bqHHPb"] / div / div / div / div[1] / a[2] / div / span')
                        netflix_news_tab.click()
        print('news tab clicked')

        ### custom range - 18.01.01 ~ 23.12.31
        '''
        18년~23년까지 범위를 설정해도 30페이지까지밖에 검색되지 않음 -> 한달 단위로 끊어서 크롤링 -> 총 66개 구간, 300개씩 >> 19800개
        1/1/2018~2/1/2018, ~~~ , 11/2/2023~12/1/2023, 12/2/2023~1/1/2024
        '''
        # month,year = list(range(1,12)),list(range(2018,2024))
        # for y in year:
        i = 0
        for m in month:
            start_date = f'{m}/2/{year}'
            if (year == 2018) & (m == 1):
                start_date = f'{m}/1/{year}'
            end_date = f'{m+1}/1/{year}'
            if (m == 11):
                end_date = f'1/1/{year+1}'

            # click tools button for the first time
            # if start_date == '1/1/2018':
            if i == 0:
                tool_btn = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="hdtb-tls"]')))
                tool_btn.click()
                i+=1
            try:
                recent_btn = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ow55"]/div[1]/div/div/div')))
                recent_btn.click()
            except (TimeoutException,NoSuchElementException) as rbtn_e:
                try:
                    recent_btn = driver.find_element(By.XPATH,'//*[@id="tn_1"]/span[1]/g-popup/div[1]/div/div/div')
                    recent_btn.click()
                except Exception:
                    try:
                        recent_btn = driver.find_element(By.XPATH,'// *[ @ id = "ow35"] / div[1] / div / div / div')
                    except Exception:
                        print('No recent_button')
            time.sleep(random.randint(2, 5)) #### randomly sleep for avoiding restriced
            custom_range_btn = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,'//*[@id="lb"]/div/g-menu/g-menu-item[8]/div/div/span')))
            custom_range_btn.click()
            # set custom search range (From, To, and click go button)
            start_date_input = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="OouJcb"]')))
            end_date_input = driver.find_element(By.XPATH, '//*[@id="rzG2be"]')
            go_btn = driver.find_element(By.XPATH, '//*[@id="T3kYXe"]/g-button')
            if start_date != '1/1/2018': # 처음이 아니면 기존의 날짜값들을 지워줘야 함
                driver.execute_script("document.querySelector('#OouJcb').value=''")
                driver.execute_script("document.querySelector('#rzG2be').value=''")
                pass
            start_date_input.send_keys(start_date)
            end_date_input.send_keys(end_date)
            go_btn.click()
            ### finished customising date range

            print(f"start_date : {start_date}, end_date : {end_date}")

            ### iterate 30 pages
            page = 1
            while (1):
                time.sleep(random.randint(2,4)) #### randomly sleep for avoiding restriced
                if page != 1:
                    page_navigator_tds = driver.find_elements(By.XPATH,'//*[@id="botstuff"]/div/div[3]/table/tbody/tr/td')
                    for p in page_navigator_tds:
                        try:
                            a = p.find_element(By.CSS_SELECTOR, 'a')
                            if a.text == f'{page}':
                                a.click()
                                break
                        except (TimeoutException, NoSuchElementException) as a_e:
                            continue
                print('page: ',page)
                ### scrap news title, url, date by pages
                selector = '#rso > div > div > div'
                divs = driver.find_elements(By.CSS_SELECTOR,selector)
                for div in divs:
                    article = div.find_element(By.CSS_SELECTOR,'div > div > a')
                    articles_url.append(article.get_attribute('href'))
                    articles_title.append(article.find_element(By.CSS_SELECTOR,'div > div.SoAPf > div.n0jPhd.ynAwRc.MBeuO.nDgy9d').text)
                    date = article.find_element(By.CSS_SELECTOR,'div > div.SoAPf > div.OSrXXb.rbYSKb.LfVVr > span').text
                    date = parse_date_format(date)
                    articles_date.append(date)
                if page == 30:
                    break
                page += 1
            ### end while
        ### end inner for

    except (TimeoutException, NoSuchElementException) as e :
        print('지정한 요소를 찾을 수 없음.')
        print(e)
    except Exception as e_:
        print("기타 에러")
        print(e_)
    finally:
        # 에러 발생 시에도 df객체 파일로 저장 가능하도록 코딩
        articles_df = pd.DataFrame(data=[articles_title,articles_date,articles_url])
        articles_df = articles_df.transpose().rename(columns={0:'title',1:'date',2:'url'})
        driver.quit()
        return articles_df
