import joblib
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="makes predictions with an ML model")
parser.add_argument("--input-path", dest="input_path", help="input path to read the model from", default="model.joblib")
parser.add_argument("--output-path", dest="output_path", help="output path to write the predictions to", default="predictions.csv")
args = parser.parse_args()

X = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
])
model = joblib.load(args.input_path)
y = model.predict(X)
Xy = np.append(X, y.reshape(-1, 1), axis=1)
np.savetxt(args.output_path, Xy, delimiter=",")
