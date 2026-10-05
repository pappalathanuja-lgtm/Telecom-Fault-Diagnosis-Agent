"""Deterministic, stateful generator for simulated tower telemetry."""
from __future__ import annotations

from datetime import datetime, timezone
from random import Random
from typing import Any


class TelemetryGenerator:
    """Produces repeatable telemetry samples without blocking Streamlit."""

    STAGES = ("NORMAL", "DEGRADATION", "ANOMALY", "FAULT", "RECOVERY")

    def __init__(self, seed: int = 23) -> None:
        self.random = Random(seed)
        self.sample_number = 0

    def next_sample(self, tower_id: str, stage: str | None = None) -> dict[str, Any]:
        self.sample_number += 1
        stage = stage or self.STAGES[min((self.sample_number - 1) // 3, len(self.STAGES) - 1)]
        r = self.random
        value: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(), "tower_id": tower_id,
            "latency_ms": round(max(1, r.gauss(22, 3)), 1), "packet_loss": round(max(0, r.gauss(.5, .25)), 2),
            "signal_strength": round(min(1, max(0, r.gauss(.86, .035))), 3), "error_rate": round(max(0, r.gauss(.3, .2)), 2),
            "cpu_load": round(min(1, max(0, r.gauss(.38, .08))), 3), "temperature": round(r.gauss(42, 2), 1),
            "power_ok": 1, "link_down": 0, "connectivity_status": "CONNECTED", "traffic_load": round(r.uniform(.25, .75), 3),
            "affected_node": None, "failed_link": None, "stage": stage,
        }
        if stage == "DEGRADATION":
            value.update(latency_ms=round(r.uniform(58, 78), 1), packet_loss=round(r.uniform(4, 9), 1), signal_strength=round(r.uniform(.52, .68), 2), traffic_load=round(r.uniform(.72, .86), 2))
        elif stage == "ANOMALY":
            value.update(latency_ms=round(r.uniform(90, 130), 1), packet_loss=round(r.uniform(10, 19), 1), cpu_load=round(r.uniform(.78, .94), 2), error_rate=round(r.uniform(8, 16), 1))
        elif stage == "FAULT":
            value.update(latency_ms=round(r.uniform(150, 195), 1), packet_loss=round(r.uniform(65, 95), 1), link_down=1, connectivity_status="DEGRADED", affected_node=tower_id, failed_link="L05")
        elif stage == "RECOVERY":
            value.update(latency_ms=round(r.uniform(24, 35), 1), packet_loss=round(r.uniform(.5, 2), 1), signal_strength=round(r.uniform(.78, .9), 2), connectivity_status="RECOVERING")
        return value
