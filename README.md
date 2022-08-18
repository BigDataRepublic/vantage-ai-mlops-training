# Vantage AI MLOps Training

## Day 1: Workflow orchestration with Airflow

### 1. Installation

Make sure you have Helm and a local Kubernetes instance running. 
Then, run:

```bash
./install.sh
```

Also, create a virtual environment and install the `requirements.txt` inside.

### 2. Inspect Hello World DAG

1. Inspect the `dags/hello_world.py` file and try to understand it
2. Port-forward the web server service via Lens or via
```bash
kubectl port-forward -n airflow svc/airflow-webserver 8080:8080
```
3. Explore the Airflow UI in your browser
4. Activate the hello_world DAG and explore it

### 3. ML Pipeline Orchestration

The `ml` folder contains scripts for training an ML model and making predictions with it.
They are packaged in an image called `ml-vantage`.
The scripts have arguments for input and output paths.

Use the `KubernetesPodOperator` to create an ML pipeline DAG.
It should run on a weekly basis.
It should first train an ML model and then make predictions with it.
Use the provided `PersistentVolumeClaim` `ml` as external storage.

After building the DAG, update the DAGs in Airflow with the following command:
```bash
./update-dags.sh
```

Then, activate the DAG and get it to work. 
You can exec into the `ml-pvc-inspector` pod in the `airflow` namespace to inspect the `PersistentVolumeClaim`.
You can peek at the solution in the `dags` folder if you get stuck. 

## Day 2: Experiment tracking with MLflow

### 1. Setup

Follow the setup from day 1. 
If you have day 1 installed on your machine already, the following will be sufficient
```bash
kubectl apply -f k8s.yaml
```

There are also new dependencies in the `requirements.txt`, so you should update your virtual environment for local development.

### 2. Upgrading the scripts to MLflow

Port-forward the mlflow and S3 services via Lens or via
```bash
kubectl port-forward -n mlflow svc/mlflow 5000:5000
kubectl port-forward -n mlflow svc/s3 9000:9000
```

Upgrade `ml/train.py` such that the training runs are recorded in MLflow.
- To be able to connect to the services on kubernetes, export the following environment variables
```bash
export MLFLOW_TRACKING_URI="http://localhost:5000"
export AWS_ACCESS_KEY_ID=foo
export AWS_SECRET_ACCESS_KEY=bar
export MLFLOW_S3_ENDPOINT_URL="http://localhost:9000"
```
- Define the experiment using `mlflow.set_experiment`
- Start a new run using `with mlflow.start_run`
- Log the model using `mlflow.sklearn.log_model`
- Add other interesting information to MLflow

Also upgrade `ml/predict.py` such that it pulls the correct model from MLflow.
You could use `mlflow.search_runs` to find the relevant run, and `mlflow.sklearn.load_model` to load the model.

Lastly, orchestrate the new scripts via Airflow by upgrading the ml pipeline DAG from last week.
Inside the pods, the URLs to MLflow and S3 are different:
```bash
MLFLOW_TRACKING_URI="http://mlflow.mlflow:5000"
MLFLOW_S3_ENDPOINT_URL="http://s3.mlflow:9000"
```

If you get stuck, you can look at `ml/mlflow_solution` and `dags/mlflow_solution.py` for inspiration.
