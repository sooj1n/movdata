from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.empty import EmptyOperator

from airflow.operators.python import (
        PythonOperator,
        PythonVirtualenvOperator,
        BranchPythonOperator
)

with DAG(
    'movies_dynamic_json',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(seconds=3),
    },
    schedule="@once",
    max_active_runs=1,
    max_active_tasks=3,
    description='movie_data_spark',
    #schedule_interval=timedelta(days=1),
    start_date=datetime(2019, 1, 1),
    #end_date=datetime(2015,1,7),
    catchup=True,
    tags=['dynamic','movie','json'],
) as dag:
    
    def fun_getdata(dt):
        print('*'*1000)
        print(dt)
        from movdata.get_data import save_movies
        save_movies(dt)


    start=EmptyOperator(task_id='start')

    get_data = PythonVirtualenvOperator(
            task_id='get.data',
            python_callable=fun_getdata,
            requirements=["git+https://github.com/sooj1n/movdata.git@0.2.1/airflow"],
            op_args=["{{ ds[:4] }}"],
            system_site_packages=False
    )

    parsing_parquet = BashOperator(
            task_id='parsing.parquet',
            bash_command="""
                echo "parsing"
            """
    
    )

    select_parquet = BashOperator(
            task_id='select.parquet',
            bash_command="""
                echo "select"
            """
    )

    end=EmptyOperator(task_id='end')

    start >> get_data >> parsing_parquet >> select_parquet >> end
