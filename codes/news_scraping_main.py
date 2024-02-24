### ⚠️Install the latest version of Selenium
from news_web_scraping.news_scraping_chrome import *
from tqdm import tqdm

years = list(range(2018,2024))
months = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]

if __name__ == '__main__':
    for year in years:
        for month in tqdm(months):
            articles_df = netflix_news_scraping_s2e(year,month)
            articles_df.to_csv(f'../data/scraping/articles_urls_{year}_{month[0]}.csv')
            '''
            articles_df have ['title','date','url'] columns
            '''
    print('end scraping')
