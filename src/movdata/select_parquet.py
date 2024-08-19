"""select.parquet.py"""

from pyspark.sql.functions import count
from pyspark.sql import SparkSession
import sys

APP_NAME = sys.argv[1]
YEAR = sys.argv[2]

spark = SparkSession.builder.appName(APP_NAME).getOrCreate()

g = spark.read.parquet("/home/sujin/code/movdata/data/movies/year=2019/goal_data")
#g.show()

# 회사별 영화 개수
result = g.groupBy('companyNm').agg(count('movieCd').alias('movie_count'))
print("회사별 영화 개수")
result.show()

# 장르별 회사 개수
result = g.groupBy('repGenreNm').agg(count('companyNm').alias('company_count'))
print('장르별 회사 개수')
result.show()

# 감독별 영화 수
result = g.groupBy('peopleNm').agg(count('movieCd').alias('movie_cnt'))
print('감독별 영화 수')
result.show()

spark.stop()
