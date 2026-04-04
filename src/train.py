import mlflow, pandas as pd, joblib
from lightgbm import LGBMClassifier
from features import build_features

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("uplift-model")

df = build_features()
y = df["target"]
treatment = df["treatment_flg"]
X = df.drop(["target","treatment_flg","client_id"], axis=1)
joblib.dump(X.columns.tolist(), "feature_columns.pkl")

X_treat, y_treat = X[treatment==1], y[treatment==1]
X_control, y_control = X[treatment==0], y[treatment==0]

with mlflow.start_run():
    mt = LGBMClassifier()
    mc = LGBMClassifier()
    mt.fit(X_treat,y_treat)
    mc.fit(X_control,y_control)

    mlflow.sklearn.log_model(mt,"model_treat")
    mlflow.sklearn.log_model(mc,"model_control")

    joblib.dump(mt,"model_treat.pkl")
    joblib.dump(mc,"model_control.pkl")
