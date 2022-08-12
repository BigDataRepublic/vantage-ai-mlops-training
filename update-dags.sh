set -e

docker build -t airflow-vantage .
kubectl delete pod -n airflow -l component=worker
kubectl delete pod -n airflow -l component=webserver
kubectl delete pod -n airflow -l component=scheduler
kubectl delete pod -n airflow -l component=triggerer
