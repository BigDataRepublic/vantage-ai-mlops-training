import mlflow
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="makes predictions with an ML model")
parser.add_argument("--datetime", dest="datetime", help="datetime belonging to the run", default="2021-01-01")
parser.add_argument("--output-path", dest="output_path", help="output path to write the predictions to", default="predictions.csv")
args = parser.parse_args()

runs = mlflow.search_runs(experiment_names=["mlops-training"], filter_string=f"tags.ds = '{args.datetime}'", output_format="list")
run_id = runs[0].info.run_id
model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")

X = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
])
y = model.predict(X)
Xy = np.append(X, y.reshape(-1, 1), axis=1)
np.savetxt(args.output_path, Xy, delimiter=",")
