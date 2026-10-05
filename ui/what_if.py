"""Interactive multi-scenario what-if and resilience analysis."""
import pandas as pd
import streamlit as st
from python_engine.what_if import SCENARIOS, simulate
from python_engine.route_analysis import analyze_routes
from python_engine.resilience import calculate_resilience

MITIGATION = {
 "Tower Outage":"Dispatch field inspection; reroute services across surviving links.",
 "Link Failure":"Repair the failed span and route traffic through the computed alternate path.",
 "Multiple Tower Outage":"Prioritize critical-site restoration and reduce nonessential traffic on surviving paths.",
 "Multiple Link Failure":"Repair the highest-impact spans first; verify alternate-route connectivity before restoration.",
 "High Traffic / Congestion":"Apply traffic shaping and rebalance load across available capacity.",
 "Hardware Failure":"Inspect tower equipment, cooling and alarm counters; prepare a controlled component replacement.",
 "Power Failure":"Check mains, rectifier, batteries and generator; validate tower recovery before reconnecting links.",
}

def render_what_if(nodes, links, run_graph, render_topology) -> None:
    st.subheader("What-If Simulation & Alternative Route Analysis")
    scenario = st.selectbox("Scenario", SCENARIOS)
    tower_options = [node["tower_id"] for node in nodes]
    link_options = [link["link_id"] for link in links]
    towers = st.multiselect("Affected tower(s)", tower_options, default=tower_options[:1] if scenario not in ("Link Failure", "Multiple Link Failure") else [])
    link_ids = st.multiselect("Failed link(s)", link_options, default=link_options[:1] if scenario == "Link Failure" else [])
    source, destination = st.columns(2)
    src = source.selectbox("Route source", tower_options, index=0)
    dst = destination.selectbox("Route destination", tower_options, index=min(6, len(tower_options) - 1))
    if st.button("RUN WHAT-IF ANALYSIS", type="primary"):
        if src == dst:
            st.error("Choose different source and destination towers for route analysis.")
            return
        changed_nodes, changed_links, telemetry = simulate(scenario, towers, link_ids, nodes, links)
        try:
            failed_towers = {telemetry.get("affected_node")} if scenario in ("Tower Outage", "Power Failure") else set(towers) if scenario == "Multiple Tower Outage" else set()
            start = src if src not in failed_towers else next((node["tower_id"] for node in nodes if node["tower_id"] not in failed_towers), src)
            graph = run_graph({"nodes": changed_nodes, "links": changed_links, "start": start})
            routes = analyze_routes(changed_nodes, links, changed_links, src, dst, run_graph)
            resilience = calculate_resilience(graph, changed_nodes, changed_links, routes["available"])
        except Exception as exc:
            st.error(f"Scenario analysis failed: {exc}")
            return
        ratio = len(graph["affected_nodes"]) / max(1, len(nodes))
        impact = "High" if ratio >= .4 or telemetry["latency_ms"] >= 150 or telemetry["power_ok"] == 0 else "Moderate" if ratio >= .15 or telemetry["latency_ms"] >= 75 or telemetry["cpu_load"] >= .82 else "Low"
        metrics = st.columns(5)
        metrics[0].metric("REACHABLE TOWERS", f"{len(graph['visited_nodes'])}/{len(nodes)}")
        metrics[1].metric("UNREACHABLE TOWERS", len(graph["affected_nodes"]))
        metrics[2].metric("FAILED LINKS", len(graph["affected_links"]))
        metrics[3].metric("RESILIENCE", f"{resilience['score']}% · {resilience['label']}")
        metrics[4].metric("ESTIMATED IMPACT", impact)
        st.markdown("#### Resilience score breakdown")
        st.write(resilience["formula"])
        st.dataframe(pd.DataFrame([{"Reachability contribution / 50":resilience["reachable_contribution"],"Available-link contribution / 30":resilience["link_contribution"],"Alternate-route contribution / 20":resilience["route_contribution"],"Score":resilience["score"],"Interpretation":resilience["label"]}]), hide_index=True, width="stretch")
        st.markdown("#### Alternative route")
        st.write("Route before failure:", " → ".join(routes["primary_route"]) if routes["primary_route"] else "No baseline route")
        st.write("Route after failure:", " → ".join(routes["alternative_route"]) if routes["alternative_route"] else "UNREACHABLE — no route remains")
        st.write(f"Rerouting possible: **{'YES' if routes['available'] else 'NO'}** · baseline hops {routes['primary_hops']} · after-failure hops {routes['alternative_hops']}")
        st.write("Affected links:", ", ".join(routes["affected_links"]) or "None")
        st.write("Alternate links:", ", ".join(routes["alternate_links"]) or "None")
        st.markdown("#### Telemetry impact and mitigation")
        st.json(telemetry)
        st.write(MITIGATION[scenario])
        st.markdown("#### Java graph result")
        st.write("DFS:", " → ".join(graph["dfs_path"]))
        st.write("BFS levels:")
        st.json(graph["bfs_levels"])
        render_topology(changed_links)
