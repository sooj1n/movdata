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
    'movies-dynamic-json',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(seconds=3),
    },
    max_active_runs=1,
    max_active_tasks=3,
    description='movie_data_spark',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2015, 1, 1),
    end_date=datetime(2015,1,7),
    catchup=True,
    tags=['dynamic','movie','json'],
) as dag:


    start=EmptyOperator(task_id='start')
    get_data=EmptyOperator(task_id='get.data')
    parsing_parquet=EmptyOperator(task_id='parsing.parquet')
    select_parquet=EmptyOperator(task_id='select.parquet')
    end=EmptyOperator(task_id='end')

    start >> get_data >> parsing_parquet >> select_parquet >> end
