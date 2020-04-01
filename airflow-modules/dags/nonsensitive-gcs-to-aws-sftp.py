import os

from airflow import models
from airflow.models import DAG

from datetime import datetime, timedelta


from operators.gcs_to_sftp_operator import GCSToSFTPOperator
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='nonsensitive-gcs-to-aws-sftp',
    default_args=default_args,
    start_date=datetime.utcnow(),
    schedule_interval='@once'
)


copy_file_from_gcs_to_sftp = GCSToSFTPOperator(
    task_id="file-copy-gsc-to-sftp",
    gcs_bucket='dlp-nonsensitive-data-bucket-cust01',
    gcs_dest='sample_n01.txt',
    sftp_dest_path='/home/ec2-user/from-gcp',
    google_cloud_storage_conn_id='my_gcp_conn',
    sftp_conn_id='my_sftp_conn'

)


log_message = BashOperator(
    task_id='print_message',
    bash_command='ls -l /usr/local/airflow/out/dlp-test-data.csv; echo "$(date --iso-8601=seconds) hello, it should work" > /usr/local/airflow/copy_file_from_gcs_to_sftp.txt',
    dag=dag)


copy_file_from_gcs_to_sftp >> log_message
