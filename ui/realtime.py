"""Streamlit-compatible continuously refreshed simulated telemetry page."""
from __future__ import annotations
import time
import pandas as pd
import streamlit as st
from python_engine.telemetry_generator import TelemetryGenerator


def render_realtime_page(nodes: list[dict], links: list[dict], do_analysis) -> None:
    st.subheader("Simulated Real-Time Telemetry")
    st.caption("Synthetic tower samples refresh through a Streamlit fragment; no blocking loop or network device is involved.")
    tower = st.selectbox("Tower", [node["tower_id"] for node in nodes], key="rt_tower")
    speed = st.select_slider("Sample interval", options=[1, 2, 3, 5], value=2, format_func=lambda value: f"{value} sec", key="rt_speed")
    st.session_state.setdefault("rt_running", False)
    st.session_state.setdefault("rt_history", [])
    if "rt_generator" not in st.session_state:
        st.session_state.rt_generator = TelemetryGenerator()
    if "rt_next_at" not in st.session_state:
        st.session_state.rt_next_at = 0.0

    @st.fragment(run_every=1)
    def telemetry_panel():
        cols = st.columns(3)
        if cols[0].button("Start Simulation", disabled=st.session_state.rt_running, key="rt_start"):
            st.session_state.rt_running = True
            st.session_state.rt_next_at = 0.0
        if cols[1].button("Stop Simulation", disabled=not st.session_state.rt_running, key="rt_stop"):
            st.session_state.rt_running = False
        refresh = cols[2].button("Refresh / Generate Next Sample", key="rt_refresh")
        now = time.monotonic()
        should_sample = refresh or (st.session_state.rt_running and now >= st.session_state.rt_next_at)
        if should_sample:
            sample = st.session_state.rt_generator.next_sample(tower)
            st.session_state.rt_current_sample = sample
            st.session_state.rt_history.append(sample)
            st.session_state.rt_history = st.session_state.rt_history[-250:]
            st.session_state.rt_next_at = now + speed
        sample = st.session_state.get("rt_current_sample")
        if sample is None:
            sample = st.session_state.rt_generator.next_sample(tower, "NORMAL")
            st.session_state.rt_current_sample = sample
        severity = "red" if sample["link_down"] or not sample["power_ok"] else "green" if sample["latency_ms"] < 80 and sample["packet_loss"] < 10 else "orange"
        st.markdown(f"**Sample state:** :{severity}[{sample['stage']}] · generated {sample['timestamp']}")
        values = [("LATENCY", f"{sample['latency_ms']} ms"), ("PACKET LOSS", f"{sample['packet_loss']}%"), ("SIGNAL", f"{sample['signal_strength']:.2f}"), ("CPU", f"{sample['cpu_load']:.0%}"), ("TEMPERATURE", f"{sample['temperature']} °C"), ("POWER", "ON" if sample["power_ok"] else "OFF"), ("LINK", "DOWN" if sample["link_down"] else "UP"), ("CONNECTIVITY", sample["connectivity_status"]), ("TRAFFIC LOAD", f"{sample['traffic_load']:.0%}")]
        metric_cols = st.columns(3)
        for index, (label, value) in enumerate(values):
            metric_cols[index % 3].metric(label, value)
        st.dataframe(pd.DataFrame([sample]), hide_index=True, width="stretch")
        if st.button("Send current sample to diagnosis", key="rt_diagnose"):
            diagnosis_input = {key: sample[key] for key in ("latency_ms", "packet_loss", "signal_strength", "error_rate", "cpu_load", "temperature", "power_ok", "link_down", "affected_node", "failed_link")}
            graph_links = [dict(link) for link in links]
            for link in graph_links:
                if link["link_id"] == sample.get("failed_link"):
                    link["status"] = "DOWN"
            do_analysis(diagnosis_input, nodes, graph_links)
        if st.session_state.rt_history:
            with st.expander("Recent telemetry history"):
                st.dataframe(pd.DataFrame(st.session_state.rt_history[-20:]), hide_index=True, width="stretch")
    telemetry_panel()
