from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client.models import V1Volume, V1VolumeMount, V1PersistentVolumeClaimVolumeSource
from datetime import timedelta, datetime

MODEL_PATH = "/mnt/ml/model.joblib"
IMAGE = "ml-vantage:latest"
NAMESPACE = "airflow"
VOLUME = V1Volume(
    name="ml",
    persistent_volume_claim=V1PersistentVolumeClaimVolumeSource(
        claim_name="ml"
    )
)
VOLUME_MOUNT = V1VolumeMount(
    name="ml",
    mount_path="/mnt/ml"
)

with DAG(
        dag_id="ml_pipeline_solution",
        schedule_interval=timedelta(weeks=1),
        start_date=datetime(2021, 1, 1),
        catchup=False,
) as dag:
    train = KubernetesPodOperator(
        task_id="train",
        name="train",
        image=IMAGE,
        namespace=NAMESPACE,
        volumes=[VOLUME],
        image_pull_policy="Never",
        volume_mounts=[VOLUME_MOUNT],
        arguments=["train.py", "--output-path", MODEL_PATH]
    )
    predict = KubernetesPodOperator(
        task_id="predict",
        name="predict",
        image=IMAGE,
        namespace=NAMESPACE,
        volumes=[VOLUME],
        image_pull_policy="Never",
        volume_mounts=[VOLUME_MOUNT],
        arguments=["predict.py", "--input-path", MODEL_PATH, "--output-path", "/mnt/ml/predictions.csv"]
    )

    train >> predict
