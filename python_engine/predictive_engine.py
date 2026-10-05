"""Transparent prototype risk estimation using generated telemetry history."""
from typing import Any


def predict_maintenance(tower_id: str, history: list[dict[str, Any]]) -> dict[str, Any]:
    samples = [row for row in history if row.get("tower_id") == tower_id]
    if not samples:
        return {"tower_id": tower_id, "score": 0.0, "category": "LOW", "factors": ["No abnormal historical samples recorded"], "action": "Continue routine monitoring."}
    latest = samples[-1]
    values = {
        "temperature": min(1, max(0, (float(latest.get("temperature", 40)) - 45) / 55)),
        "CPU load": min(1, max(0, (float(latest.get("cpu_load", 0)) - .55) / .45)),
        "error rate": min(1, float(latest.get("error_rate", 0)) / 40),
        "packet loss": min(1, float(latest.get("packet_loss", 0)) / 40),
        "latency": min(1, float(latest.get("latency_ms", 0)) / 180),
        "signal degradation": 1 - min(1, float(latest.get("signal_strength", 1))),
        "repeated anomalies": min(1, sum(row.get("anomaly_status") == "ANOMALOUS" for row in samples) / max(1, len(samples))),
    }
    score = round(100 * sum(values.values()) / len(values), 1)
    category = "HIGH" if score >= 65 else "MEDIUM" if score >= 35 else "LOW"
    factors = [name for name, value in sorted(values.items(), key=lambda pair: pair[1], reverse=True) if value >= .35]
    action = "Schedule maintenance inspection and review alarm history." if category == "HIGH" else "Review trends at the next maintenance window." if category == "MEDIUM" else "Continue routine monitoring."
    return {"tower_id": tower_id, "score": score, "category": category, "factors": factors or ["No individual signal exceeded the review threshold"], "action": action, "formula": "Mean of normalized temperature, CPU, errors, loss, latency, signal degradation and repeated-anomaly indicators."}
