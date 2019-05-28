import pandas as pd
import numpy as np
import seaborn as sns
from bs4 import BeautifulSoup
import requests
import logging
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

# STEP 1: get wikipedia links to feed into scraper
# not necessary for new wikipedia titles run after initial training of model
class get_wiki_links:

    def __init__(self):
        self.wiki_titles = []
        self.wiki_urls = []
        self.wiki_api_titles = []
    
    def fit(self,start_year,end_year):
        logging.info('Getting wikipedia links...')
        self.get_links(start_year, end_year)
        logging.info('Clean wikipedia URLs...')
        self.clean_wiki_urls()
        logging.info('Setting up dataframes...')
        self.data_frames()
        logging.info('Complete!')
           
    def get_links(self,start_year,end_year):
        for year in range(start_year,end_year + 1):
            url = 'https://en.wikipedia.org/wiki/' + str(year) + '_in_film'
            result = requests.get(url)
            soup = BeautifulSoup(result.content, 'html5lib')
            links = soup.find_all("table", { "class" : "wikitable sortable" })

            for link in links:
                for lin in link.find_all('i'):
                    for i in lin.find_all('a'):
                        self.wiki_titles.append(i.get_text())
                        self.wiki_urls.append(i.get('href'))

    def clean_wiki_urls(self):    
        for url in self.wiki_urls:
            org_url = url
            url = url.replace('%27', "'")
            url = url.replace('%26', '&')
            url = url.replace('%28', '(')
            url = url.replace('%29', ')')
            url = url.replace('%3F', '?')
            url = url.replace('%E2%80%93', '-')
            url = url.replace('%C3%A9', 'é')
            url = url.replace('%C3%A8', 'è')
            url = url.replace('%2C', ',')
            url = url.replace('%C4%97', 'ė')
            url = url.replace('%C3%A0', 'à')
            url = url.replace('%C3%BC', 'ü')
            url = url.replace('%C3%A1', 'á')
            self.wiki_api_titles.append((org_url,url[6:]))

    def data_frames(self):
        #create dataframe for wiki link and titles, not really needed, might remove
        self.df_wiki_links = pd.DataFrame({'wiki_url': self.wiki_urls,
                                           'wiki_title': self.wiki_titles})
        df_wiki_links_clean = pd.DataFrame(self.wiki_api_titles,columns=['org_wiki_url','clean_wiki_url'])
        self.df_wiki_links = self.df_wiki_links.merge(df_wiki_links_clean,left_on='wiki_url',right_on='org_wiki_url',how='left')
        self.df_wiki_links = self.df_wiki_links.drop_duplicates(subset=['wiki_url'])
        self.df_wiki_links.to_csv('data/wikipedia_links.csv',sep=',',index=False)