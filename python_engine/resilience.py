"""Explainable network resilience calculation from observed graph properties."""
from typing import Any

REACHABILITY_WEIGHT = 0.50
LINK_AVAILABILITY_WEIGHT = 0.30
ALTERNATE_ROUTE_WEIGHT = 0.20

def calculate_resilience(graph_result: dict[str, Any], nodes: list[dict], links: list[dict], alternate_route_available: bool) -> dict[str, Any]:
    total_nodes = max(1, len(nodes)); total_links = max(1, len(links))
    reachable = len(graph_result.get("visited_nodes", [])) / total_nodes
    link_availability = sum(str(link.get("status", "UP")).upper() == "UP" for link in links) / total_links
    route = 1.0 if alternate_route_available else 0.0
    score = round(100 * (REACHABILITY_WEIGHT * reachable + LINK_AVAILABILITY_WEIGHT * link_availability + ALTERNATE_ROUTE_WEIGHT * route))
    label = "Excellent" if score >= 90 else "Good" if score >= 75 else "Moderate" if score >= 55 else "Poor" if score >= 30 else "Critical"
    return {"score": score, "label": label, "reachable_contribution": round(100 * REACHABILITY_WEIGHT * reachable, 1), "link_contribution": round(100 * LINK_AVAILABILITY_WEIGHT * link_availability, 1), "route_contribution": round(100 * ALTERNATE_ROUTE_WEIGHT * route, 1), "reachable_ratio": reachable, "link_availability": link_availability, "alternate_route_available": alternate_route_available, "formula": f"100 × ({REACHABILITY_WEIGHT:.2f} × reachable tower ratio + {LINK_AVAILABILITY_WEIGHT:.2f} × available link ratio + {ALTERNATE_ROUTE_WEIGHT:.2f} × alternate route availability)"}
