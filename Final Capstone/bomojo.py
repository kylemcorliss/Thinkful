from bs4 import BeautifulSoup
import requests
from cache_to_disk import cache_to_disk
import pandas as pd

def get_nth_tag_text(tree, tag, n):
	try:
		return tree.find_all(tag)[n].get_text(strip=True)
	except:
		return None

def get_item_nth_tag_text(tree, pos, tag, n):
	try:
		return tree[pos].find_all(tag)[n].get_text(strip=True)
	except:
		return None

# get request and then return items from bomojo page
@cache_to_disk('data/bomojo.pkl')     
def get_data(url):
	try:
		result = requests.get(url)
		soup = BeautifulSoup(result.content,features='html5lib')
		figures = soup.find_all('div', {'class': 'mp_box_content'})

		return {
		'bomojo_url' : url,  #bomojo url as primary key
		'title' : get_nth_tag_text(soup, 'b', 1),
		'genre' : get_nth_tag_text(soup, 'b', 5),
		'release_date' : get_nth_tag_text(soup, 'b', 4),
		'rating' : get_nth_tag_text(soup, 'b', 7),
		'distributor' : get_nth_tag_text(soup, 'b', 3),
		'dom_box_office' : get_item_nth_tag_text(figures, 0, 'b', 1),
		'ww_box_office' : get_item_nth_tag_text(figures, 0, 'b', 4),
		'op_wkd_box_office' : get_item_nth_tag_text(figures, 1, 'td', 1),
		'num_theaters' : get_item_nth_tag_text(figures, 1, 'tr', 4)
		}
	except:
		return {'bomojo_url' : url}

def clean_df(df):
	replace_chars = ['Widest\xa0Release:',' theaters', ',']
	datetime_cols = ['release_date']
	replace_cols = ['dom_box_office','ww_box_office','op_wkd_box_office']
	numeric_cols = ['dom_box_office', 'ww_box_office','op_wkd_box_office', 'num_theaters']

	for c in replace_chars:
		df['num_theaters'] = df['num_theaters'].replace(c, '', regex=True)     
	for d in datetime_cols:
		df[d] = pd.to_datetime(df[d],errors='coerce')        
	for r in replace_cols:
		df[r] = df[r].replace('[\$,]', '', regex=True)
	for n in numeric_cols:
		df[n] = pd.to_numeric(df[n],errors='coerce')

	return df
