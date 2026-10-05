"""Primary NOC pages: Home, tower inspection and multi-fault injection."""
import pandas as pd
import streamlit as st
from python_engine.resilience import calculate_resilience
from python_engine.simulation_engine import inject_multiple
from ui.diagnosis_view import render_diagnosis

FAULT_TYPES=["Fiber Link Failure","Tower Power Failure","Hardware Failure","High Latency","Packet Loss","Signal Degradation","Network Congestion"]

def render_home(nodes, baseline_links, incidents, saved_events, render_topology):
    latest=saved_events[0] if saved_events else None
    shown_links=latest["links"] if latest else baseline_links
    graph=latest["incident"].get("graph_result",{}) if latest else {"visited_nodes":[n["tower_id"] for n in nodes]}
    down=sum(edge["status"]!="UP" for edge in shown_links)
    health=round(100*len(graph.get("visited_nodes",[]))/max(1,len(nodes))*(1-down/max(1,len(shown_links))))
    resilience=calculate_resilience(graph,nodes,shown_links,bool(graph.get("route_path",True)))
    anomaly=latest["incident"].get("evidence",{}).get("anomaly",{}).get("status","NORMAL") if latest else "NORMAL"
    avg=round(sum(event["diagnosis_time_ms"] for event in incidents)/max(1,len(incidents)))
    cols=st.columns(8)
    vals=[f"{health}/100",len(nodes),len(shown_links)-down,len(incidents),sum(x["severity"]=="CRITICAL" for x in incidents),f"{avg} ms",f"{resilience['score']}%",anomaly]
    labels=["NETWORK HEALTH","TOWERS","ACTIVE LINKS","INCIDENTS","CRITICAL","AVG DIAG TIME","RESILIENCE","ANOMALY STATUS"]
    for col,label,value in zip(cols,labels,vals): col.metric(label,value)
    left,right=st.columns([1.5,1])
    with left: st.subheader("LIVE NETWORK TOPOLOGY"); render_topology(shown_links)
    with right:
        st.subheader("RECENT INCIDENTS")
        if incidents: st.dataframe(pd.DataFrame(incidents)[["incident_id","fault_type","severity","confidence","root_cause"]].head(8),hide_index=True,width="stretch")
        else: st.success("No simulated incidents yet. The synthetic baseline network is healthy.")
    st.caption("Synthetic academic demonstration topology and telemetry.")

def render_network_noc(nodes, baseline_links, incidents, saved_events, render_topology):
    st.subheader("Network Operations Center")
    tower=st.selectbox("Inspect tower",[node["tower_id"] for node in nodes])
    latest=saved_events[0] if saved_events else None
    links=latest["links"] if latest else baseline_links
    event=latest["incident"] if latest else None
    telemetry=latest["telemetry"] if latest and latest["telemetry"].get("affected_node")==tower else None
    selected_links=[edge for edge in links if tower in (edge["source"],edge["destination"])]
    render_topology(links,tower)
    record=next(node for node in nodes if node["tower_id"]==tower)
    health="CRITICAL" if telemetry and (not telemetry.get("power_ok",1) or telemetry.get("link_down",0)) else "WARNING" if telemetry and (telemetry.get("latency_ms",0)>=80 or telemetry.get("packet_loss",0)>=10) else "HEALTHY"
    graph=event.get("graph_result",{}) if event else {"visited_nodes":[node["tower_id"] for node in nodes]}
    down=sum(edge["status"]!="UP" for edge in links)
    network_health=round(100*len(graph.get("visited_nodes",[]))/max(1,len(nodes))*(1-down/max(1,len(links))))
    a,b,c,d,e=st.columns(5);a.metric("TOWER HEALTH",health);b.metric("CONNECTED LINKS",len(selected_links));c.metric("FAILED LINKS",sum(edge["status"]!="UP" for edge in selected_links));d.metric("ACTIVE ALARMS",1 if event and event.get("affected_node")==tower else 0);e.metric("NETWORK HEALTH",f"{network_health}%")
    st.markdown("#### Tower telemetry")
    if telemetry: st.json(telemetry)
    else: st.dataframe(pd.DataFrame([record]),hide_index=True,width="stretch")
    st.markdown("#### Link health")
    status=st.multiselect("Link status filter",["UP","DOWN"],default=["UP","DOWN"])
    st.dataframe(pd.DataFrame([edge for edge in selected_links if edge["status"] in status]),hide_index=True,width="stretch")
    if incidents:
        history=[incident for incident in incidents if incident.get("affected_node")==tower]
        st.markdown("#### Diagnosis history")
        st.dataframe(pd.DataFrame(history),hide_index=True,width="stretch")
    failed=[edge["link_id"] for edge in links if edge["status"]!="UP"]
    st.write("Network status:",f"{len(nodes)-len(event.get('fault_path',[])) if event else len(nodes)} reachable towers · failed links: {', '.join(failed) or 'none'}")

def render_fault_simulation(nodes, links, do_analysis):
    st.subheader("Fault Injection Lab")
    selected=st.multiselect("Fault conditions to inject simultaneously",FAULT_TYPES,default=["Fiber Link Failure"])
    tower=st.selectbox("Affected tower",[node["tower_id"] for node in nodes])
    link=st.selectbox("Link (used for fiber failure)",[edge["link_id"] for edge in links])
    if st.button("INJECT FAULT & DIAGNOSE",type="primary"):
        if not selected:
            st.error("Select at least one fault condition.")
        else:
            telemetry,changed_nodes,changed_links=inject_multiple(selected,tower,link,nodes,links)
            if do_analysis(telemetry,changed_nodes,changed_links): st.success("Completed telemetry, Java graph, rules, anomaly, ML, root-cause ranking and incident storage.")
    render_diagnosis(st.session_state.current)

def render_diagnosis_page(current, explain=False):
    st.subheader("Explainable Fault Diagnosis" if explain else "Latest Fault Diagnosis")
    render_diagnosis(current)
    if explain:
        st.info("The page displays recorded rule conditions, class probabilities, anomaly score and Java graph results. It does not expose hidden chain-of-thought.")
