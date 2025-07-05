from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'brentford',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='dlt_to_snowflake_dagv2003',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['Liverpool', 'bronze', 'dlt'],
) as dag:

    run_dlt_pipeline = BashOperator(
        task_id='run_dlt_pipeline',
        bash_command='python  /opt/airflow/etl_pipeline/sql_database_pipeline.py',
    )

    run_dlt_pipeline