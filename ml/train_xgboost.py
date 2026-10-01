import pandas as pd
import joblib

from sklearn.model_selection import train_test_split

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


df = pd.read_csv(
    "data/raw/transactions.csv"
)

X = df.drop(
    "is_fraud",
    axis=1
)

y = df["is_fraud"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


negative = (y_train == 0).sum()
positive = (y_train == 1).sum()

scale_pos_weight = (
    negative / positive
)


model = XGBClassifier(

    n_estimators=200,

    max_depth=5,

    learning_rate=0.05,

    scale_pos_weight=
        scale_pos_weight,

    random_state=42,

    eval_metric="logloss"
)


model.fit(
    X_train,
    y_train
)


predictions = model.predict(
    X_test
)


print(
    "Accuracy:",
    accuracy_score(
        y_test,
        predictions
    )
)

print(
    "Precision:",
    precision_score(
        y_test,
        predictions,
        zero_division=0
    )
)

print(
    "Recall:",
    recall_score(
        y_test,
        predictions,
        zero_division=0
    )
)

print(
    "F1:",
    f1_score(
        y_test,
        predictions,
        zero_division=0
    )
)


joblib.dump(
    model,
    "models/xgboost_model.pkl"
)

print(
    "XGBoost model saved."
)