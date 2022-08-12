# Airflow Handson

## 1. Installation

```bash
./install.sh
```

Also, create a virtual environment and install the `requirements.txt` inside.

## 2. Inspect Hello World DAG

1. Inspect the `dags/hello_world.py` file and try to understand it
2. Port-forward the web server service via Lens or via
```bash
kubectl port-forward -n airflow svc/airflow-webserver 8080:8080
```
3. Explore the Airflow UI in your browser
4. Activate the hello_world DAG and explore it

## 3. ML Pipeline Orchestration

The `ml` folder contains scripts for training an ML model and making predictions with it.
They are packaged in an image called `ml-vantage`.
The scripts have arguments for input and output paths.

Use the `KubernetesPodOperator` to create an ML pipeline DAG.
It should run on a weekly basis.
It should first train an ML model and then make predictions with it.
Use the provided PersistentVolumeClaim `ml` as external storage.

After building the DAG, update the DAGs in Airflow with the following command:
```bash
./update-dags.sh
```

Then, activate the DAG and get it to work. 
You can exec into the ml-pvc-inspector pod to inspect the PersistentVolumeClaim.
You can peek at the solution in the `dags` folder if you get stuck. 
