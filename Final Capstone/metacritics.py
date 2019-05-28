from bs4 import BeautifulSoup
import requests
from cache_to_disk import cache_to_disk
import pandas as pd

@cache_to_disk('data/metacritic.pkl')       
def get_score(url):

	if url.endswith("/"):
		url_review = url + 'critic-reviews'
	else:
		url_review = url + '/critic-reviews'
	try:
		headers = {'User-Agent': 'Mozilla/5.0'}
		result = requests.get(url_review, headers=headers)
		soup = BeautifulSoup(result.content,features='html5lib')
		score = soup.find_all('td', {'class' : 'num_wrapper'})
		# scores = soup.find_all('div', {'class': 'metascore_w'}) 
		# dates = soup.find_all('span', {'class': 'date'})

		# reviews = []
		# if not dates:
		# 	for score in scores:
		# 		reviews.append({
		# 			# 'index': index, 
		# 			'url' : url, 
		# 			'date' : None, 
		# 			'score' : score.get_text(strip=True)
		# 			})
		# else:
		# 	for date, score in zip(dates,scores):
		# 		reviews.append({
		# 			# 'index': index, 
		# 			'url' : url, 
		# 			'date' : date.get_text(strip=True), 
		# 			'score' : score.get_text(strip=True)
		# 			})
		# return reviews

		# just get the overall calculated score rather than each review as in the above
		return {
		'url' : url,
		'score' : int(score[0].get_text(strip=True))
		}

	except:
		return {
				# 'index': index, 
				'url' : url, 
				# 'date' : None, 
				'score' : None}
 


# def clean_df(df):
# 	df['mc_score'] = pd.to_numeric(df['mc_score'],errors='coerce')
# 	return df.groupby(['wiki_url'],as_index=True).mean()



