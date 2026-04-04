# import joblib, pandas as pd

# mt = joblib.load("model_treat.pkl")
# mc = joblib.load("model_control.pkl")

# def predict_uplift(data):
#     df = pd.DataFrame([data])
#     return float(mt.predict_proba(df)[0][1] - mc.predict_proba(df)[0][1])
import pandas as pd
import joblib

def load_models():
    mt = joblib.load("model_treat.pkl")
    mc = joblib.load("model_control.pkl")
    return mt, mc

def build_single_feature(client_id):
    clients = pd.read_csv("data/clients.csv")

    row = clients[clients["client_id"] == client_id]

    # same preprocessing as training
    row["first_issue_date"] = pd.to_datetime(row["first_issue_date"], errors="coerce")
    row["first_redeem_date"] = pd.to_datetime(row["first_redeem_date"], errors="coerce")

    row["days_between"] = (
        row["first_redeem_date"] - row["first_issue_date"]
    ).dt.days

    row["days_between"] = row["days_between"].fillna(0)

    row = row.drop(["first_issue_date", "first_redeem_date"], axis=1)

    row = pd.get_dummies(row, columns=["gender"], dummy_na=True)

    row = row.fillna(0)

    row = row.drop(["client_id"], axis=1)

    return row


def predict_uplift(client_id):
    mt, mc = load_models()

    X = build_single_feature(client_id)

    # ✅ LOAD TRAINING SCHEMA
    cols = joblib.load("feature_columns.pkl")

    # ✅ ALIGN FEATURES
    X = X.reindex(columns=cols, fill_value=0)

    p1 = mt.predict_proba(X)[0][1]
    p0 = mc.predict_proba(X)[0][1]

    return float(p1 - p0)