import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest


df = pd.read_csv(
    "data/raw/transactions.csv"
)


features = df[
    [
        "amount"
    ]
]


model = IsolationForest(

    n_estimators=200,

    contamination=0.05,

    random_state=42
)


model.fit(features)


joblib.dump(
    model,
    "models/isolation_forest.pkl"
)

print(
    "Isolation Forest model saved."
)