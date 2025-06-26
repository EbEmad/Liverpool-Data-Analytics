from airflow.operators.bash import BashOperator
from datetime import datetime

default_args={
    'owner':'Liverpool',
    'start_date': datetime(2025,6,25),
    'retries':1
}
with DAG(
    dag_id='scrape_to_postgres_dag',
    default_args=default_args,
    schedule='@daily',
    catchup=False
) as dag:
    scrape_and_load=BashOperator(
        task_id='scrape_and_load',
        bash_command='python /opt/airflow/scripts/scrap.p'
    )