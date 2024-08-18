import requests
import os
import json
import time
from tqdm import tqdm

API_KEY = os.getenv("MOVIE_API_KEY")

def save_json(data, file_path):
	# 파일저장 경로 MKDIR
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def req(url):
    r = requests.get(url)
    j = r.json()
    return j

def save_company(year,company_list,sleep_time):
	file_path = f'data/movies/year={year}/company.json'

	# 위 경로가 있으면 API 호출을 멈추고 프로그램 종료
	if os.path.exists(file_path):
		print(f"데이터가 이미 존재합니다: {file_path}")
		return True

	# 토탈카운트 가져오고 total_pages 계산
	url_base = f"http://kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyList.json?key={API_KEY}"
	
	all_data=[]
	for c in tqdm(company_list):
		time.sleep(sleep_time)
		r = req(url_base + f"&companyNm={c}")
		d = r['companyListResult']['companyList']
		all_data.extend(d)
	
	save_json(all_data, file_path)
	return all_data


def load_json(year):
	file_path = f'data/movies/year={year}/data.json'
	with open(file_path, 'r', encoding='utf-8') as f:
		data = json.load(f)

	company_list = []
	for movie in data:
		for company in movie['companys']:
			company_list.append(company['companyNm'])

	save_company(year,company_list,0.1)
	return company_list
