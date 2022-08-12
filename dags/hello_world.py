from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta, datetime

with DAG(
    dag_id="hello_world",
    schedule_interval=timedelta(minutes=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
) as dag:
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )
    t2 = BashOperator(
        task_id="sleep",
        bash_command="sleep 5",
    )
    t3 = BashOperator(
        task_id="templated",
        depends_on_past=False,
        bash_command="echo '{{ ds }}'",
    )

    t1 >> [t2, t3]
