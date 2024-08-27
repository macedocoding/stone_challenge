import duckdb
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta
from docker.types import Mount
from dotenv import load_dotenv
from google.cloud import storage


YESTERDAY = datetime.now() - timedelta(days=1)
BUCKET_NAME = 'desafio-eng-dados'
LOCAL_PATH = os.path.join(os.path.abspath(os.path.join(os.getcwd(), '../../')), 'blobs')
PREFIX = '2024'


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'start_date': YESTERDAY,
}

with DAG(
        'pipeline',
        catchup=False,
        default_args=default_args,
        schedule_interval='@daily') as dag:


    def download_blobs(*kwargs):
            storage_client = storage.Client()
            bucket = storage_client.bucket(BUCKET_NAME)
            blobs = bucket.list_blobs(prefix=PREFIX)

            for blob in blobs:
                blob_name = blob.name
                blob_path = os.path.join(LOCAL_PATH, blob_name)
                blob.download_to_filename(blob_path)


    def duckdb_insert():
        load_dotenv('/home/macedo/Projetos/stone_challenge/config_files/conf.env')
        conn = duckdb.connect()

        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        dbname = os.getenv('DB_NAME')

        conn.execute(f"ATTACH 'postgresql://{user}:{password}@{host}:{port}/{dbname}' AS db (TYPE POSTGRES);")
        conn.execute("""
            CREATE OR REPLACE TEMP TABLE original AS
            SELECT * FROM read_parquet('/home/macedo/Projetos/stone_challenge/blobs/2024*')
            """)
        
        conn.execute("""
            INSERT INTO db.public.technicians (
                technician_email
            )
            SELECT
                distinct(technician_email)
            FROM original
            """)
        
        conn.execute("""
            INSERT INTO db.public.providers (
                provider
            )
            SELECT
                distinct(provider)
            FROM original
            """)
        
        conn.execute("""
            INSERT INTO db.public.customers (
                customer_id, customer_phone, city, country, country_state, zip_code, street_name, complement, neighborhood
            )
            SELECT
                distinct(customer_id), customer_phone, city, country, country_state, zip_code, street_name, complement, neighborhood
            FROM original
            """)
        
        conn.execute("""   
            INSERT INTO db.public.terminals (
                terminal_id, provider_id, technician_id, terminal_serial_number, terminal_model, terminal_type
            )
            SELECT
                distinct(terminal_id),
                provider_id,
                technician_id,
                terminal_serial_number, 
                terminal_model, 
                terminal_type, 
            FROM original
                JOIN db.public.providers
                    ON original.provider = providers.provider
                JOIN db.public.technicians
                    ON original.technician_email = technicians.technician_email;
            """)
        
        conn.execute("""
            INSERT INTO db.public.orders (
                order_number, terminal_id, customer_id, cancellation_reason, last_modified_date, arrival_date, deadline_date
            )
            SELECT
                order_number, terminal_id, customer_id, cancellation_reason, last_modified_date, arrival_date, deadline_date
            FROM original
            """)


########################################################################################################


    download_blobs_task = PythonOperator(
        task_id='download_blobs_task',
        provide_context=True,
        python_callable=download_blobs,
    )

    duckdb_insert_task = PythonOperator(
        task_id='duckdb_insert_task',
        python_callable=duckdb_insert,
        dag=dag)


download_blobs_task >> duckdb_insert_task
