"""Fault injection helpers operating on copies of the baseline synthetic topology."""
import copy

BASE_TELEMETRY={"latency_ms":20,"packet_loss":.5,"signal_strength":.84,"error_rate":.2,"cpu_load":.4,"temperature":42,"power_ok":1,"link_down":0}

def inject(fault, node, link, nodes, links):
    t=dict(BASE_TELEMETRY); ns=copy.deepcopy(nodes); es=copy.deepcopy(links)
    if fault=="Fiber Link Failure":
        selected=next((e for e in es if e["link_id"]==link),es[0]);selected["status"]="DOWN";t.update(link_down=1,packet_loss=92,latency_ms=180,error_rate=38,failed_link=selected["link_id"],affected_node=selected["destination"])
    elif fault=="Tower Power Failure":
        t.update(power_ok=0,signal_strength=.1,packet_loss=85,affected_node=node)
        for edge in es:
            if node in (edge["source"],edge["destination"]): edge["status"]="DOWN"
    elif fault=="Hardware Failure":t.update(cpu_load=.97,temperature=91,error_rate=34,affected_node=node)
    elif fault=="High Latency":t.update(latency_ms=155,affected_node=node)
    elif fault=="Packet Loss":t.update(packet_loss=32,affected_node=node)
    elif fault=="Signal Degradation":t.update(signal_strength=.22,affected_node=node)
    elif fault=="Network Congestion":t.update(cpu_load=.94,latency_ms=115,affected_node=node)
    return t,ns,es

def inject_multiple(faults, node, link, nodes, links):
    """Compose simultaneous symptom profiles while preserving independent graph changes."""
    telemetry=dict(BASE_TELEMETRY); changed_nodes=copy.deepcopy(nodes); changed_links=copy.deepcopy(links)
    for fault in faults:
        profile, _, graph_links=inject(fault,node,link,changed_nodes,changed_links)
        for key,value in profile.items():
            if key not in BASE_TELEMETRY or value != BASE_TELEMETRY[key]:
                telemetry[key]=value
        changed_links=graph_links
    return telemetry,changed_nodes,changed_links

def predictive_risk(telemetry):
    # Transparent prototype heuristic based on normalized measured thresholds, not an ML failure forecast.
    terms=[min(1,max(0,telemetry.get("latency_ms",20)/180)),min(1,max(0,telemetry.get("packet_loss",0)/50)),1-telemetry.get("signal_strength",.85),telemetry.get("cpu_load",.3),max(0,(telemetry.get("temperature",40)-35)/60),1-telemetry.get("power_ok",1)]
    score=100*sum(terms)/len(terms)
    return {"score":round(score,1),"level":"HIGH" if score>=65 else "MEDIUM" if score>=35 else "LOW"}
