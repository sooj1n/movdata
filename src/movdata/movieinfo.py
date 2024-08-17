import requests
import os
import json
import time
from tqdm import tqdm

API_KEY = os.getenv("MOVIE_API_KEY")
def save_json(year,all_data):
	file_path = f'data/movies/year={year}/movieinfo.json'
	
	#파일저장 경로 MKDIR
	os.makedirs(os.path.dirname(file_path), exist_ok=True)

	with open(file_path, 'w', encoding='utf-8') as f:
		json.dump(all_data, f, indent=4, ensure_ascii=False)


def req(url):
    r = requests.get(url)
    j = r.json()
    return j


def load_json(year):
	file_path = f'data/movies/year={year}/data.json'
	with open(file_path, 'r', encoding='utf-8') as f:
		data = json.load(f)

	movie_codes = [movie['movieCd'] for movie in data]
	save_data(year,movie_codes)
	return movie_codes

def save_data(year,movie_codes,sleep_time=1):
	#file_path = f'data/movies/year={year}/movieinfo.json'
	url_base = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={API_KEY}'
	all_data = []
	for code in tqdm(movie_codes):
		time.sleep(sleep_time)
		r = req(url_base + f"&movieCd={code}")
		d = r['movieInfoResult']['movieInfo']
		all_data.extend(d)

	save_json(year,all_data)
	return True


