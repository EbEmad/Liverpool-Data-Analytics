from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow import DAG

default_args={
    'owner':'Liverpool',
    'start_date': datetime(2025,6,28),
    'retries':1
}
with DAG(
    dag_id='scrape_to_postgres_dagv2',
    default_args=default_args,
    schedule='@daily',
    catchup=False
) as dag:
    scrape_and_load=BashOperator(
        task_id='scrape_and_load',
        bash_command='python /opt/airflow/scripts/scrap.py'
    )