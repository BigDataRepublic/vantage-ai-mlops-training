FROM apache/airflow

COPY ./dags/ ${AIRFLOW_HOME}/dags/
