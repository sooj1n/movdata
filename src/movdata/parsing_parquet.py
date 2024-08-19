"""parsing.parquet.py"""

from pyspark.sql import SparkSession
import sys

APP_NAME = sys.argv[1]
YEAR = sys.argv[2]

spark = SparkSession.builder.appName(APP_NAME).getOrCreate()

# pyspark 에서 multiline(배열) 구조 데이터 읽기
jdf = spark.read.option("multiline","true").json(f"/home/sujin/code/movdata/data/movies/year={YEAR}/airflow_data.json")

# 펼치기
from pyspark.sql.functions import explode, col, size
edf = jdf.withColumn("company", explode("companys"))

# 또 펼치기
eedf = edf.withColumn("director", explode("directors"))

"""
eedf.select("movieCd", "company", "director").printSchema()
root
 |-- movieCd: string (nullable = true)
 |-- company: struct (nullable = true)
 |    |-- companyCd: string (nullable = true)
 |    |-- companyNm: string (nullable = true)
 |-- director: struct (nullable = true)
 |    |-- peopleNm: string (nullable = true)

"""
# 또 또 펼치기
goal_df = eedf.select("movieCd","repGenreNm","repNationNm", "company.companyNm", "director.peopleNm")
goal_df.show()

goal_df.write.parquet(f"/home/sujin/code/movdata/data/movies/year={YEAR}/goal_data")

spark.stop()
