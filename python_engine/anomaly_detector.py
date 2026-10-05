"""Anomaly detection identifies unusual telemetry; it does not name a fault."""
from sklearn.ensemble import IsolationForest
from .classifier import dataset, FEATURES

def train_detector():
    x, _ = dataset(per_class=80)
    return IsolationForest(contamination=.12, random_state=42).fit(x)

def detect(model, telemetry):
    vector = [[float(telemetry.get(k, d)) for k, d in zip(FEATURES, [20, 0, .85, 0, .3, 40, 1, 0])]]
    score = float(model.decision_function(vector)[0])
    label = model.predict(vector)[0]
    return {"status": "ANOMALOUS" if label == -1 else ("SUSPICIOUS" if score < .04 else "NORMAL"), "score": score}
