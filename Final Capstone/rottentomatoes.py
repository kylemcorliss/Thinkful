from bs4 import BeautifulSoup
import requests
from cache_to_disk import cache_to_disk

# # function to return dictionary based on the items and tags passed to it
# # only needed if runing function to get individual critic reviews
# def return_dict(url, name, date, icon):
# 	name.find_all('a')
# 	return {
# 	'rt_url' : url,
# 	'critic_name' : name.get_text("|",strip=True),
# 	'date' : date.get_text(strip=True),
# 	'rt-icon' : icon.get('class')[3]
# 	}


#cleaning function to replace %s, strings, etc. from beautifulsoup item passed to function
def fallback(string, pos):
	try:
		string = string[pos].get_text(strip=True)
	except:
		return 0
	string = string.split('%')[0]
	string = string.replace(',', '')
	try:
		return int(string)
	except:
		return 0

# function to scrape rottentomatoes page for critic and viewer scores
@cache_to_disk('data/rottentomatoes.pkl')
def get_score(url):
	
	# # function to get the individual critic reviews that make up the score
	# if url.endswith("/"):
	# 	url_top = url + 'reviews/?type=top_critics'
	# else:
	# 	url_top = url + '/reviews/?type=top_critics'
	
	# # first request to get critic reviews
	# result = requests.get(url_top)
	# soup = BeautifulSoup(result.content, 'html.parser')
	# figures = soup.find_all('div', {'class': 'review_table'})

	# names = figures[0].find_all('div', {'class': 'critic_name'}) # name of people and journal
	# dates = figures[0].find_all('div',{'class': 'review_date subtle small'}) # review date
	# icons = figures[0].find_all('div',{'class': 'review_icon'})

	# critic_reviews = []

	# for name, date, icon in zip(names,dates,icons):
	# 	reviews.append(return_dict(url, name, date, icon))

	# second request to get audience reviews
	result = requests.get(url)
	soup = BeautifulSoup(result.content, features='html5lib')
	reviews = soup.find_all('span', {'class': 'mop-ratings-wrap__percentage'})
	counts = soup.find_all('small', {'class' : 'mop-ratings-wrap__text--small'})
	return {
	'url' : url,
	'critic_score' : fallback(reviews, 0),
	'critic_counts' : fallback(counts, 0),
	'aud_score' : fallback(reviews, 1),
	'aud_counts' : fallback(counts, 1)
	}



# def clean_df(df):
# 	# # only necessary with function to get individual critic reviews
# 	# df = pd.get_dummies(data=df, columns=['rt_review'])
# 	# df = df.groupby(['wiki_url'],as_index=True).mean()


# 	return df
