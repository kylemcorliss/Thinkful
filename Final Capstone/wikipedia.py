from bs4 import BeautifulSoup
import requests
from cache_to_disk import cache_to_disk
from mwviews.api import PageviewsClient
import datetime
import pandas as pd
import numpy as np


# function to iterate through all hyperlinks on wiki page and return bomojo, rottentomatoes, metacritics, imdb
@cache_to_disk('data/wiki_links.pkl')
def get_wiki_links(url):
	dictionary = {}
	dictionary['wiki_url'] = url 
	try: 
		result = requests.get('https://en.wikipedia.org/' + url)
		soup = BeautifulSoup(result.content, features='html5lib')

		# get external links for bomojo, imdb, metacritic, rottentomatoes for each title and add it to dictionary
		ext_text = soup.find_all('a', {'class': 'external text'})
		ext_links = []
		for ext in ext_text:
			ext_links.append(ext.get('href'))

		# ad hoc way to parse out links for each title and site
		for link in ext_links:
			if 'mojo' in link:
				if 'movies' in link:
					dictionary['bomojo_link'] = link
				else:
					pass
			elif 'rottentomatoes' in link:
				if 'editorial' in link:
					pass
				elif 'archive' in link:
					pass
				else:
					dictionary['rottentomatoes_link'] = link
			elif 'metacritic' in link:
				if 'user' in link:
					pass
				elif 'imdb' in link:
					pass
				elif 'rotten' in link:
					pass
				elif 'archive' in link:
					pass
				else:
					dictionary['metacritic_link'] = link
			elif 'imdb' in link:
				if 'soundtrack' in link:
					pass
				elif 'metacritic' in link:
					pass
				elif 'rotten' in link:
					pass
				elif 'archive' in link:
					pass
				else:
					dictionary['imdb_link'] = link
			else:
				pass

		return dictionary  
	except:
		return dictionary
    

# with clean urls, run each title through wikipedia api to get search volume
@cache_to_disk('data/wiki_pageviews.pkl')
def get_wiki_pageviews(title):
	p = PageviewsClient(user_agent="<person@organization.org> multiple movie titles")
	today = datetime.datetime.now().strftime("%Y%m%d")
	try:
		return p.article_views('en.wikipedia', title, start='20130101',end=today)
	except:
		return {}


# function to create features from pageview data based on release date
def clean_pageviews(df, df1, url, title):

	row = {}
	row['title'] = title
	row['wiki_url'] = url

	if title not in df:
		return row

	series = df[title]
	row['mean_total'] = series.mean()
	row['max_total'] = series.max()
	row['median_total'] = series.median()
	row['std_total'] = series.std()

	if url not in df1.index:
		return row

	release_date = df1[df1.index == url]['release_date'].values[0]
	if np.isnat(release_date):
		return row

	for week in [2,3,4]:
		date_range = pd.date_range(start = (release_date - pd.Timedelta(days=(week+1)*7-1)),end = (release_date - pd.Timedelta(days=(week+1)*7-7)))                
		
		if min(date_range) < min(series.index):
			return row
		if max(date_range) > max(series.index):
			return row

		subset = series.loc[date_range]
		if len(subset) > 0:
			row[f'mean_week_{week}'] = subset.mean()
			row[f'max_week_{week}'] = subset.max()
			row[f'median_week_{week}'] = subset.median()
			row[f'std_week_{week}'] = subset.std()
		else:
			None
	for month in [2,3]:
		date_range = pd.date_range(start = (release_date - pd.Timedelta(days=month*30-1)),end = (release_date - pd.Timedelta(days=month*30-30)))

		if min(date_range) < min(series.index):
			return row
		if max(date_range) > max(series.index):
			return row

		subset = series.loc[date_range]
		if len(subset) > 0:
			row[f'mean_month_{month}'] = subset.mean()
			row[f'max_month_{month}'] = subset.max()
			row[f'median_month_{month}'] = subset.median()
			row[f'std_month_{month}'] = subset.std()
		else:
			None
			
	return row