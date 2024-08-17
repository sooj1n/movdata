from movdata.ml import save_movies

def test_save_movies():
	for y in range(2015,2022):
		r = save_movies(year=y, sleep_time=0.1)
	assert r
        
