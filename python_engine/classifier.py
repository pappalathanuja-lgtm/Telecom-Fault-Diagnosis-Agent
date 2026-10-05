"""Train a local fault classifier on reproducible synthetic telemetry."""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

FEATURES = ["latency_ms", "packet_loss", "signal_strength", "error_rate", "cpu_load", "temperature", "power_ok", "link_down"]
LABELS = ["Normal", "Fiber Link Failure", "Tower Power Failure", "Hardware Failure", "High Latency", "Packet Loss", "Signal Degradation", "Network Congestion"]

def dataset(seed=19, per_class=160):
    rng = np.random.default_rng(seed)
    rows, labels = [], []
    for label in LABELS:
        for _ in range(per_class):
            x = [rng.normal(20, 5), rng.uniform(0, 2), rng.normal(.84, .07), rng.uniform(0, 1), rng.uniform(.2, .7), rng.normal(42, 5), 1, 0]
            if label == "Fiber Link Failure": x[0], x[1], x[3], x[7] = rng.normal(180, 25), rng.uniform(65, 100), rng.uniform(25, 60), 1
            elif label == "Tower Power Failure": x[6], x[2], x[1] = 0, rng.uniform(0, .2), rng.uniform(70, 100)
            elif label == "Hardware Failure": x[4], x[5], x[3] = rng.uniform(.93, 1), rng.uniform(82, 110), rng.uniform(20, 70)
            elif label == "High Latency": x[0] = rng.uniform(120, 250)
            elif label == "Packet Loss": x[1] = rng.uniform(18, 60)
            elif label == "Signal Degradation": x[2] = rng.uniform(.05, .38)
            elif label == "Network Congestion": x[4], x[0] = rng.uniform(.82, 1), rng.uniform(75, 150)
            rows.append(x); labels.append(label)
    return np.asarray(rows), np.asarray(labels)

def train_model():
    x, y = dataset()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=140, max_depth=12, class_weight="balanced", random_state=42)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    return model, {"accuracy": accuracy_score(y_test, pred), "precision_macro": precision_score(y_test, pred, average="macro", zero_division=0), "recall_macro": recall_score(y_test, pred, average="macro", zero_division=0), "f1_macro": f1_score(y_test, pred, average="macro", zero_division=0), "report": classification_report(y_test, pred, output_dict=True, zero_division=0), "matrix": confusion_matrix(y_test, pred, labels=LABELS), "labels": LABELS}

def classify(model, telemetry):
    vector = [[float(telemetry.get(k, d)) for k, d in zip(FEATURES, [20, 0, .85, 0, .3, 40, 1, 0])]]
    probs = model.predict_proba(vector)[0]
    idx = int(np.argmax(probs))
    return {"fault_type": str(model.classes_[idx]), "confidence": float(probs[idx]), "probabilities": {str(k): float(v) for k, v in zip(model.classes_, probs)}}
