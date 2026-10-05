"""Orchestrates evidence from rules, ML, anomaly detection, and Java graph search."""
from datetime import datetime, timezone
from uuid import uuid4
from .rule_engine import diagnose as run_rules
from .classifier import classify
from .anomaly_detector import detect

def analyze(telemetry, nodes, links, model, anomaly_model, graph_fn):
    rules=run_rules(telemetry); ml=classify(model,telemetry); anomaly=detect(anomaly_model,telemetry)
    failed=next((link for link in links if link.get("link_id")==telemetry.get("failed_link")),None)
    affected=telemetry.get("affected_node")
    # Start from the healthy side of a failed link, or a non-affected tower for tower outages.
    if failed:
        start=failed["source"]
    else:
        start=next((node["tower_id"] for node in nodes if node["tower_id"] != affected), nodes[0]["tower_id"])
    destination=next((node["tower_id"] for node in nodes if node["tower_id"] != start), start)
    graph=graph_fn({"nodes":nodes,"links":links,"start":start,"destination":destination})
    # Rank candidate types using both deterministic rule strength and the classifier's measured class probability.
    candidates=[]
    for rule in rules:
        classifier_probability=ml["probabilities"].get(rule["fault_type"],0.0)
        anomaly_weight = .03 if anomaly["status"] == "ANOMALOUS" else .015 if anomaly["status"] == "SUSPICIOUS" else 0.0
        candidates.append({**rule,"classifier_probability":classifier_probability,"anomaly_weight":anomaly_weight,"combined_score":max(0.0, min(.99, .65*rule["score"]+.35*classifier_probability+anomaly_weight))})
    if not candidates: candidates=[{"fault_type":ml["fault_type"],"score":0,"severity":"MAJOR","evidence":[],"recommended_action":"Inspect telemetry and topology.","classifier_probability":ml["confidence"],"combined_score":.35*ml["confidence"]}]
    candidates.sort(key=lambda item:item["combined_score"],reverse=True)
    chosen=candidates[0]
    confidence=min(.99, chosen["combined_score"])
    root=(f"{failed['source']}–{failed['destination']} Fiber Link Failure" if failed and chosen["fault_type"]=="Fiber Link Failure" else telemetry.get("affected_node") or chosen["fault_type"])
    ranked=[{"fault_type":item["fault_type"],"confidence":min(.99,item["combined_score"]),"severity":item["severity"],"evidence":item["evidence"],"recommended_action":item["recommended_action"],"rule_score":item["score"],"classifier_probability":item["classifier_probability"],"anomaly_weight":item.get("anomaly_weight",0.0)} for item in candidates]
    secondary=[item for item in ranked[1:] if item["fault_type"]!="Normal"]
    recommendations=list(dict.fromkeys(item["recommended_action"] for item in ranked if item["fault_type"]!="Normal")) or [chosen["recommended_action"]]
    event={"incident_id":"INC-"+uuid4().hex[:8].upper(),"timestamp":datetime.now(timezone.utc).isoformat(),"fault_type":chosen["fault_type"],"primary_fault":{"fault_type":chosen["fault_type"],"confidence":confidence,"severity":chosen["severity"],"evidence":chosen["evidence"],"recommended_action":chosen["recommended_action"]},"secondary_faults":secondary,"confidence":confidence,"severity":chosen["severity"],"affected_node":telemetry.get("affected_node"),"affected_link":telemetry.get("failed_link"),"telemetry":telemetry,"fault_path":graph["affected_nodes"],"dfs_path":graph["dfs_path"],"bfs_result":graph["bfs_levels"],"graph_result":graph,"root_cause":str(root),"root_cause_candidates":[{"candidate":root,"confidence":confidence,"basis":["rule evidence", "classifier probability", "telemetry target", "graph reachability"]}],"ranked_candidates":ranked,"evidence":{"rule":chosen["evidence"],"graph":[f"Java DFS from {start} visited {len(graph['dfs_path'])} towers",f"Java BFS found {len(graph['affected_nodes'])} unreachable towers"],"anomaly":anomaly,"ml":ml,"telemetry":telemetry},"recommended_action":chosen["recommended_action"],"recommended_actions":recommendations,"diagnosis_time_ms":graph["dfs_time_ms"]+graph["bfs_time_ms"],"model_version":"synthetic-rf-v1"}
    return event, rules, ml, anomaly, graph
