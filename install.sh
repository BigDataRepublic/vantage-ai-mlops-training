set -e

docker build -t airflow-vantage .
docker build -t ml-vantage ml

helm repo add apache-airflow https://airflow.apache.org
helm upgrade --install airflow apache-airflow/airflow \
  --namespace airflow \
  --create-namespace \
  --set images.airflow.repository=airflow-vantage \
  --set images.airflow.tag=latest

kubectl apply -f pvc.yaml
