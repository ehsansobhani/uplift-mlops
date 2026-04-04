import pandas as pd

def build_features():
    clients = pd.read_csv("data/clients.csv")
    train = pd.read_csv("data/uplift_train.csv")

    # ---- Convert dates ----
    clients["first_issue_date"] = pd.to_datetime(clients["first_issue_date"], errors="coerce")
    clients["first_redeem_date"] = pd.to_datetime(clients["first_redeem_date"], errors="coerce")

    # Convert to numeric (days since issue)
    clients["days_between"] = (
        clients["first_redeem_date"] - clients["first_issue_date"]
    ).dt.days

    # Fill missing dates
    clients["days_between"] = clients["days_between"].fillna(0)

    # Drop raw date columns
    clients = clients.drop(["first_issue_date", "first_redeem_date"], axis=1)

    # ---- Encode categorical ----
    clients = pd.get_dummies(clients, columns=["gender"], dummy_na=True)

    # ---- Merge ----
    df = train.merge(clients, on="client_id", how="left")

    df = df.fillna(0)

    return df