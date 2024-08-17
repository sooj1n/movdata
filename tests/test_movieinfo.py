from pprint import pprint
from movdata.movieinfo import load_json
from movdata.movieinfo import save_json

def test_load():
	data = load_json('2015')
	

	assert data

