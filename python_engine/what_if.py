"""Apply real topology/symptom changes for supported what-if scenarios."""
from __future__ import annotations
from copy import deepcopy

SCENARIOS = ("Tower Outage", "Link Failure", "Multiple Tower Outage", "Multiple Link Failure", "High Traffic / Congestion", "Hardware Failure", "Power Failure")

def simulate(scenario: str, tower_ids: list[str], link_ids: list[str], nodes: list[dict], links: list[dict]) -> tuple[list[dict], list[dict], dict]:
    changed_nodes, changed_links = deepcopy(nodes), deepcopy(links)
    telemetry = {"latency_ms": 20, "packet_loss": .5, "signal_strength": .84, "error_rate": .2, "cpu_load": .4, "temperature": 42, "power_ok": 1, "link_down": 0, "traffic_load": .4}
    down_links = set(link_ids)
    down_towers = set(tower_ids)
    if scenario in ("Tower Outage", "Multiple Tower Outage", "Power Failure"):
        down_towers.update(tower_ids)
        for edge in changed_links:
            if edge["source"] in down_towers or edge["destination"] in down_towers:
                edge["status"] = "DOWN"
        telemetry.update(power_ok=0, signal_strength=.1, packet_loss=85, affected_node=next(iter(down_towers), None))
    if scenario in ("Link Failure", "Multiple Link Failure"):
        for edge in changed_links:
            if edge["link_id"] in down_links:
                edge["status"] = "DOWN"
        selected = next((edge for edge in changed_links if edge["link_id"] in down_links), None)
        if selected:
            telemetry.update(link_down=1, failed_link=selected["link_id"], affected_node=selected["destination"], latency_ms=175, packet_loss=88, error_rate=32)
    if scenario in ("High Traffic / Congestion", "Hardware Failure"):
        tower = next(iter(tower_ids), None)
        telemetry["affected_node"] = tower
        if scenario == "Hardware Failure":
            for edge in changed_links:
                if tower in (edge["source"], edge["destination"]): edge["status"] = "DOWN"
            telemetry.update(cpu_load=.98, temperature=94, error_rate=37, packet_loss=22)
    if scenario == "High Traffic / Congestion":
        telemetry.update(cpu_load=.95, latency_ms=125, traffic_load=.97, packet_loss=8)
    if scenario == "Power Failure":
        telemetry["affected_node"] = next(iter(tower_ids), None)
    return changed_nodes, changed_links, telemetry
