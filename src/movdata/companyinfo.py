import requests
import os
import json
import time
from tqdm import tqdm

API_KEY = os.getenv("MOVIE_API_KEY")

def save_json(year,all_data):
	file_path = f'data/movies/year={year}/companyinfo.json'

	#파일저장 경로 MKDIR
	os.makedirs(os.path.dirname(file_path), exist_ok=True)

	with open(file_path, 'w', encoding='utf-8') as f:
		json.dump(all_data, f, indent=4, ensure_ascii=False)


def req(url):
    r = requests.get(url)
    j = r.json()
    return j

def save_data(year,cd_list):
	url_base = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyInfo.json?key={API_KEY}'

	all_data = []
	for code in tqdm(cd_list):
		time.sleep(0.1)
		r = req(url_base + f"&companyCd={code}")
		d = r['companyInfoResult']['companyInfo']
		all_data.append(d)

	save_json(year,all_data)
	return all_data
	

def load_json(year):
	file_path = f'data/movies/year={year}/company.json'
	with open(file_path, 'r', encoding='utf-8') as f:
		data = json.load(f)

	cd_list = [company['companyCd'] for company in data]
	save_data(year,cd_list)
	return cd_list
