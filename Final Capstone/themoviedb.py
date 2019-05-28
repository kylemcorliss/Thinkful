from bs4 import BeautifulSoup
import requests
from requests import Request, Session
import time
import json
from cache_to_disk import cache_to_disk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

session = Session()
# create a prepared request to wait for 429 errors from themoviedb api
def retry(request, retry_count=5):
    prepared = request.prepare()
    response = session.send(prepared)
    if response.status_code == 429:
        time.sleep(int(response.headers['Retry-After']))
        return retry(request, retry_count-1)
    return response


@cache_to_disk("data/themoviedb_id.pkl")
def get_id(imdb_id):
    request = Request('GET', "https://api.themoviedb.org/3/find/" + imdb_id,
        params={
            "api_key": "fb2e18449dea58f15d0a8c727a8d7ee9",
            "language": "en-US",
            "external_source": "imdb_id",
        },
    )
    response = retry(request)
    result = response.json()
    if len(result["movie_results"]) == 0:
        return None
    return str(result["movie_results"][0]["id"])


# request provides movie info such as genres, budget, production companies, tagline, votes and vote scores
# not going to use the revenue and release date from here, instead use box office mojo
@cache_to_disk("data/themoviedb_detail.pkl")
def get_detail(tmdb_id):
    request = Request('GET',"https://api.themoviedb.org/3/movie/" + tmdb_id,
        params={"api_key": "fb2e18449dea58f15d0a8c727a8d7ee9", "language": "en-US"},
    )
    response = retry(request)
    return response.json()


@cache_to_disk("data/themoviedb_credits.pkl")
def get_credits(tmdb_id):
    request = Request('GET',"https://api.themoviedb.org/3/movie/" + tmdb_id + "/credits",
        params={"api_key": "fb2e18449dea58f15d0a8c727a8d7ee9"},
    )
    response = retry(request)
    result = response.json()

    return result["cast"][:4]


# request provides youtube URLs for the movie trailers, necessary to get youtube views
# will want to use result['id'] for youtube API
@cache_to_disk("data/themoviedb_video_urls.pkl")
def get_video_urls(tmdb_id):
    request = Request('GET',"https://api.themoviedb.org/3/movie/" + tmdb_id + "/videos",
        params={"api_key": "fb2e18449dea58f15d0a8c727a8d7ee9", "language": "en-US"},
    )
    response = retry(request)
    result = response.json()    

    for item in result["results"]:
        item["tmdb_id"] = tmdb_id
    return result["results"]


# get movie keywords, could be useful for vectorizer and clustering
@cache_to_disk("data/themoviedb_keywords.pkl")
def get_keywords(tmdb_id):
    request = Request('GET',"https://api.themoviedb.org/3/movie/" + tmdb_id + "/keywords",
        params={"api_key": "fb2e18449dea58f15d0a8c727a8d7ee9"},
    )
    response = retry(request)
    return response.json()


# social IDs for facebook, instagram and twitter
# not useful just yet, but maybe in the long run, so capture the info
@cache_to_disk("data/themoviedb_social_ids.pkl")
def get_social_ids(tmdb_id):
    request = Request('GET',"https://api.themoviedb.org/3/movie/" + tmdb_id + "/external_ids",
        params={"api_key": "fb2e18449dea58f15d0a8c727a8d7ee9"},
    )
    response = retry(request)
    return response.json()


# youtube / google API to get data for video links
@cache_to_disk("data/themoviedb_video_stats.pkl")
def get_video_stats(yt_id):
    request = requests.get("https://www.googleapis.com/youtube/v3/videos",
        params={
            "part": "statistics",
            "id": yt_id,
            "key": "AIzaSyACOXc4BZ-YVDaBMWSsoV4T4O_j8tRt2Aw",
        },
    )
    result = request.json()
    if len(result.get('items', {})) == 0:
        return {}
    return result['items'][0].get('statistics',{})

# run all of the functions together for one specific url
def run_tmdb(id):
    tmdb_id = get_id(id)
    if tmdb_id is None:
        return {}
    else:
        info = get_detail(tmdb_id)
        video_urls = get_video_urls(tmdb_id)
        keywords = get_keywords(tmdb_id)
        social_ids = get_social_ids(tmdb_id)
        credits = get_credits(tmdb_id)

        video_stats = []
        for video in video_urls:
            if "key" in video:
                video_stats.append(get_video_stats(video.get("key")))
                

        # need to confirm with API that there is no conflicting datapoints
        new_dict = {**info, **keywords, **social_ids, "credits" : credits, "video_stats": video_stats}

        return new_dict

# need to to a json dump so on the other side can use converters with json.loads and maintain
#dictionary structure (otherwise just a string)
def json_dump(df, *args):
    for col in args:
        df[col] = df[col].apply(json.dumps)


# tf_idf and clustering for themoviedb keywords
# too many keywords to be useful and the clusters end up being distinct enough with box office
def join_with_spaces(strs):
    return ' '.join(strs)    

def agg_keywords(df):
    return df.groupby(['wiki_url'], as_index=True).agg({'keyword': join_with_spaces})

def vectorizer(df, input_col):
    vectorizer = TfidfVectorizer(max_df=0.6, # drop words that occur in more than half the paragraphs
                             min_df=3, # only use words that appear at least three times
                             stop_words='english', 
                             lowercase=True, #convert everything to lower case
                             norm=u'l2', #correction factor so that long and short paragraphs are treated equally
                             smooth_idf=True)
    
    return vectorizer.fit_transform(df[input_col])

def cluster_movie_keywords(df,n_clusters):
    df = df.dropna()
    df_agg = agg_keywords(df)
    X_tfidf = vectorizer(df_agg, 'keyword')
    model = KMeans(n_clusters=n_clusters, random_state=42)
    y_pred = model.fit_predict(X_tfidf)

    df_agg['keyword_cluster'] = y_pred
    return df_agg, model, X_tfidf