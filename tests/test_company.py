#from movdata.company import load_json
from movdata.company import save_company
from movdata.companyinfo import load_json
from movdata.companyinfo import save_data
from pprint import pprint


'''
def test_load():
	r = load_json('2015')
	assert r


def test_save():
	r = save_company('2015',["(주)머스트씨무비릴리징컴퍼니","굿픽처스" ], 0.1)
	pprint(r)
	assert r

'''

def test_companyinfo_load():
	r = load_json('2015')
	
	assert r

#def test_save_data():
#	r = save_data('2015',['20122497','20063099'])
#	pprint(r)
#	assert r
