from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args={
    'owner':'Liverpool',
    'start_date':datetime(2025,7,1)
}

with DAG(
    dag_id='full_pipeline_dagv1',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=True,
    tags=['Liverpool','Full','ETL']
) as dag:
    #  1. Scrape & Load to PostgreSQL
    scrape_to_postgres=BashOperator(
        task_id='scrape_to_postgres',
        bash_command='cd /opt/airflow/scripts && python scrap.py'
    )

    #  2. Run dlt to load PostgreSQL → Snowflake (Bronze)
    dlt_to_snowflake = BashOperator(
        task_id='dlt_to_snowflake',
        bash_command='cd /opt/airflow/etl_pipeline && python sql_database_pipeline.py',
    )
    scrape_to_postgres>>dlt_to_snowflake