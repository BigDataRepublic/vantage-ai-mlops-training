from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay
import mlflow
from matplotlib import pyplot as plt
import argparse

parser = argparse.ArgumentParser(description="trains an ML model")
parser.add_argument("--datetime", dest="datetime", help="datetime belonging to the run", default="2021-01-01")
args = parser.parse_args()

MAX_DEPTH = 2
CONFUSION_MATRIX_PATH = "/tmp/confusion_matrix.png"

mlflow.set_experiment("mlops-training")
with mlflow.start_run(tags={"datetime": args.datetime}):
    X, y = load_iris(return_X_y=True)

    model = DecisionTreeClassifier(max_depth=MAX_DEPTH)
    mlflow.log_param("max_depth", MAX_DEPTH)

    model.fit(X, y)
    mlflow.sklearn.log_model(model, "model")

    y_pred = model.predict(X)

    train_accuracy = accuracy_score(y, y_pred)
    mlflow.log_metric("train_accuracy", train_accuracy)

    ConfusionMatrixDisplay.from_predictions(y, y_pred)
    plt.savefig(CONFUSION_MATRIX_PATH)
    mlflow.log_artifact(CONFUSION_MATRIX_PATH)
