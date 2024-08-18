import requests
import os
import json
import time
from tqdm import tqdm

API_KEY = os.getenv("MOVIE_API_KEY")

def save_json(year,all_data):
	file_path = f'data/movies/year={year}/people.json'

	#파일저장 경로 MKDIR
	os.makedirs(os.path.dirname(file_path), exist_ok=True)

	with open(file_path, 'w', encoding='utf-8') as f:
		json.dump(all_data, f, indent=4, ensure_ascii=False)


def req(url):
    r = requests.get(url)
    j = r.json()
    return j

def save_data(year,actor_list):
	url_base = f'http://kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key={API_KEY}'

	all_data = []
	for actor in tqdm(actor_list):
		time.sleep(0.1)
		r = req(url_base + f"&peopleNm={actor}")
		d = r['peopleListResult']['peopleList']
		all_data.extend(d)

	save_json(year,all_data)
	return all_data


def load_json(year):
	file_path = f'data/movies/year={year}/movieinfo.json'
	with open(file_path, 'r', encoding='utf-8') as f:
		data = json.load(f)

	actor_list=[]
	for movie in data:
		for actor in movie['actors']:
			actor_list.append(actor['peopleNm'])
			
	save_data(year,actor_list)
	return actor_list
