"""Deterministic, inspectable IF-THEN diagnostic rules."""
RULES = [
 ("Tower Power Failure", lambda t: not t.get("power_ok", 1), "Tower power telemetry reports OFF.", "Check mains supply, rectifier, and backup batteries."),
 ("Fiber Link Failure", lambda t: t.get("link_down", 0) or (t.get("packet_loss", 0) >= 60 and t.get("latency_ms", 0) >= 100), "A link is down or severe loss coincides with elevated latency.", "Inspect and restore the affected fiber segment."),
 ("Hardware Failure", lambda t: t.get("temperature", 0) >= 80 or (t.get("cpu_load", 0) >= .92 and t.get("error_rate", 0) >= 20), "Thermal or combined CPU/error threshold exceeded.", "Inspect tower hardware and cooling; review equipment alarms."),
 ("Signal Degradation", lambda t: t.get("signal_strength", 1) <= .4, "Signal strength is at or below 0.40.", "Inspect antenna alignment, interference, and radio unit."),
 ("Network Congestion", lambda t: t.get("cpu_load", 0) >= .82 and t.get("latency_ms", 0) >= 75, "High load coincides with elevated latency.", "Review traffic distribution and capacity; rebalance load."),
 ("High Latency", lambda t: t.get("latency_ms", 0) >= 100, "End-to-end latency is at least 100 ms.", "Trace the route and inspect queueing and backhaul delay."),
 ("Packet Loss", lambda t: t.get("packet_loss", 0) >= 15, "Packet loss is at least 15%.", "Check link quality, interference, and interface counters."),
]

def diagnose(t):
    found = []
    for fault, condition, evidence, action in RULES:
        try:
            if condition(t): found.append({"fault_type": fault, "score": .93 if fault in ("Fiber Link Failure", "Tower Power Failure") else .78, "severity": "CRITICAL" if fault in ("Fiber Link Failure", "Tower Power Failure", "Hardware Failure") else "MAJOR", "evidence": [evidence], "recommended_action": action})
        except (TypeError, ValueError):
            continue
    return sorted(found, key=lambda r: r["score"], reverse=True) or [{"fault_type":"Normal", "score":.72, "severity":"NORMAL", "evidence":["No configured diagnostic threshold was crossed."], "recommended_action":"Continue monitoring."}]
