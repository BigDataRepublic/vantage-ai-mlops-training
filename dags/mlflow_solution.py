from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client.models import V1Volume, V1VolumeMount, V1PersistentVolumeClaimVolumeSource, V1EnvVar
from datetime import timedelta, datetime

MODEL_PATH = "/mnt/ml/model.joblib"
IMAGE = "mlflow-vantage:latest"
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
ENV_VARS = [
    V1EnvVar("MLFLOW_TRACKING_URI", "http://mlflow.mlflow:5000"),
    V1EnvVar("MLFLOW_S3_ENDPOINT_URL", "http://s3.mlflow:9000"),
    V1EnvVar("AWS_ACCESS_KEY_ID", "foo"),
    V1EnvVar("AWS_SECRET_ACCESS_KEY", "bar"),
]

with DAG(
        dag_id="mlflow_solution",
        schedule_interval=timedelta(minutes=2),
        start_date=datetime(2021, 1, 1),
        catchup=False,
) as dag:
    train = KubernetesPodOperator(
        task_id="train",
        name="train",
        image=IMAGE,
        namespace=NAMESPACE,
        env_vars=ENV_VARS,
        volumes=[VOLUME],
        image_pull_policy="Never",
        volume_mounts=[VOLUME_MOUNT],
        arguments=["train.py", "--datetime", "{{ ts }}"]
    )
    predict = KubernetesPodOperator(
        task_id="predict",
        name="predict",
        image=IMAGE,
        namespace=NAMESPACE,
        env_vars=ENV_VARS,
        volumes=[VOLUME],
        image_pull_policy="Never",
        volume_mounts=[VOLUME_MOUNT],
        arguments=["predict.py", "--datetime", "{{ ts }}", "--output-path", "/mnt/ml/predictions.csv"]
    )

    train >> predict
