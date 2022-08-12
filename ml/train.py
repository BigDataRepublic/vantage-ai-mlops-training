from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
import joblib
import argparse

parser = argparse.ArgumentParser(description="trains an ML model")
parser.add_argument("--output-path", dest="output_path", help="output path to write the trained model to", default="model.joblib")
args = parser.parse_args()

X, y = load_iris(return_X_y=True)
model = DecisionTreeClassifier()
model.fit(X, y)
joblib.dump(model, args.output_path)
