"""Java-backed shortest-route comparison before and after simulated failures."""
from typing import Any, Callable


def analyze_routes(nodes: list[dict], baseline_links: list[dict], failed_links: list[dict], source: str, destination: str, graph_fn: Callable[[dict], dict]) -> dict[str, Any]:
    before = graph_fn({"nodes": nodes, "links": baseline_links, "start": source, "destination": destination})
    after = graph_fn({"nodes": nodes, "links": failed_links, "start": source, "destination": destination})
    primary = before.get("route_path", [])
    alternate = after.get("route_path", [])
    down_ids = {link["link_id"] for link in failed_links if str(link.get("status", "UP")).upper() != "UP"}
    route_pairs = set(zip(alternate, alternate[1:])) | set(zip(alternate[1:], alternate))
    route_ids = {link["link_id"] for link in failed_links if (link["source"], link["destination"]) in route_pairs and str(link.get("status", "UP")).upper() == "UP"}
    return {"source": source, "destination": destination, "primary_route": primary, "primary_hops": max(0, len(primary) - 1), "alternative_route": alternate, "alternative_hops": max(0, len(alternate) - 1), "available": bool(alternate), "affected_links": sorted(down_ids), "alternate_links": sorted(route_ids), "unreachable": not bool(alternate), "before_graph": before, "after_graph": after}
