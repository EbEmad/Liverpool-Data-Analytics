from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'brentford',
    'start_date': datetime(2025, 7, 5),
    'retries': 1,
}

with DAG(
    dag_id='scrape_data',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['Liverpool', 'bronze'],
) as dag:

    scrape_and_load = BashOperator(
        task_id='scrape_and_load',
        bash_command='python /opt/airflow/scripts/scrap.py',
    )

    scrape_and_load