"""Telecom Fault Diagnosis Agent — local Streamlit entry point."""

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parent / "logs" / "matplotlib"))

import pandas as pd
import streamlit as st

from python_engine.classifier import train_model
from python_engine.anomaly_detector import train_detector
from python_engine.simulation_engine import inject_multiple
from integration.java_bridge import run_graph
from utils.logger import get_logger
from ui.core_pages import render_home, render_network_noc, render_fault_simulation, render_diagnosis_page
from ui.controller import make_analysis_handler
from ui.topology import render_topology as render_topology_impl
from ui.realtime import render_realtime_page
from ui.analytics import render_analytics
from ui.academic_subjects import render_academic_subjects
from ui.traceability import render_traceability
from ui.viva_mode import render_viva
from ui.system_logs import render_system_logs
from ui.about import render_about
from ui.what_if import render_what_if

logger = get_logger()

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="TeleGuard AI | Telecom Fault Diagnosis Agent",
    page_icon="📡",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background: #08111f;
        color: #e7edf7;
    }

    .block-container {
        padding-top: 1.4rem;
        max-width: 1500px;
    }

    [data-testid="stMetric"] {
        background: #101d2d;
        border: 1px solid #22344c;
        padding: 14px;
        border-radius: 12px;
    }

    .hero {
        background: linear-gradient(110deg,#10243a,#132f43);
        border: 1px solid #24516a;
        border-radius: 16px;
        padding: 28px 34px;
        margin-bottom: 18px;
    }

    .hero h1 {
        font-size: 2.15rem;
        letter-spacing: .08em;
        margin: 0;
        color: #f2f8ff;
    }

    .hero p {
        color: #79d7df;
        font-size: 1rem;
        margin: .45rem 0 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA
# ============================================================

@st.cache_data
def data():
    from pathlib import Path

    base = Path(__file__).parent / "data"

    nodes = pd.read_csv(base / "network_nodes.csv")
    links = pd.read_csv(base / "network_links.csv")

    return nodes, links


# ============================================================
# MACHINE LEARNING MODELS
# ============================================================

@st.cache_resource
def get_model():
    """Return only the trained Random Forest model."""
    model, metrics = train_model()
    return model, metrics


@st.cache_resource
def get_anomaly_model():
    """Return the actual Isolation Forest model."""
    return train_detector()


nodes_df, links_df = data()

# Correctly unpack classifier tuple
model, metrics = get_model()

# Correctly create Isolation Forest model
anomaly_model = get_anomaly_model()

nodes = nodes_df.to_dict("records")
links = links_df.to_dict("records")

for n in nodes:
    n["tower_id"] = str(n["tower_id"])

for e in links:
    for key in ("link_id", "source", "destination", "status"):
        e[key] = str(e[key])

def render_topology(edges, focus=None):
    render_topology_impl(nodes, edges, focus)

do_analysis = make_analysis_handler(model, anomaly_model, run_graph, logger)


# ============================================================
# SESSION STATE
# ============================================================

st.session_state.setdefault("incidents", [])
st.session_state.setdefault("events", [])
st.session_state.setdefault("current", None)
st.session_state.setdefault("rt_step", 0)


# ============================================================
# SIDEBAR
# ============================================================

menu = st.sidebar.radio(
    "OPERATIONS",
    [
        "HOME",
        "NETWORK NOC",
        "FAULT DIAGNOSIS",
        "FAULT SIMULATION",
        "WHAT-IF SIMULATION",
        "SIMULATED REAL-TIME",
        "AI EXPLANATION",
        "ANALYTICS",
        "ACADEMIC SUBJECTS",
        "TRACEABILITY MATRIX",
        "VIVA MODE",
        "SYSTEM LOGS",
        "ABOUT PROJECT"
    ]
)

st.sidebar.caption("LOCAL SYNTHETIC TELEMETRY · NO CARRIER CONNECTION")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>TELECOM FAULT DIAGNOSIS AGENT</h1>
        <p>
            <b>TeleGuard AI</b> · Intelligent Network Fault Localization
            &amp; Diagnosis System
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HOMEs
# ============================================================

if menu == "HOME":
    render_home(nodes, links, st.session_state.incidents, st.session_state.events, render_topology)

elif menu == "NETWORK NOC":
    render_network_noc(nodes, links, st.session_state.incidents, st.session_state.events, render_topology)

elif menu in ("FAULT DIAGNOSIS", "AI EXPLANATION"):
    render_diagnosis_page(st.session_state.current, explain=menu == "AI EXPLANATION")

elif menu == "FAULT SIMULATION":
    render_fault_simulation(nodes, links, do_analysis)


# ============================================================
# WHAT-IF SIMULATION
# ============================================================

elif menu == "WHAT-IF SIMULATION":
    render_what_if(nodes, links, run_graph, lambda edges, focus=None: render_topology(edges, focus))


# ============================================================
# SIMULATED REAL-TIME
# ============================================================

elif menu == "SIMULATED REAL-TIME":
    st.session_state.setdefault("rt_links", links)
    render_realtime_page(nodes, links, do_analysis)

elif menu == "ANALYTICS":
    def generate_demo_incidents():
        profiles = [
            ("Fiber Link Failure", "T06", "L05"),
            ("Tower Power Failure", "T03", "L02"),
            ("Hardware Failure", "T07", "L07"),
            ("High Latency", "T02", "L01"),
            ("Packet Loss", "T04", "L03"),
            ("Signal Degradation", "T09", "L12"),
            ("Network Congestion", "T05", "L04"),
            ("Normal", "T01", "L01"),
        ]
        for fault_type, tower_id, link_id in profiles:
            telemetry, sim_nodes, sim_links = inject_multiple([fault_type], tower_id, link_id, nodes, links)
            do_analysis(telemetry, sim_nodes, sim_links)
    render_analytics(st.session_state.incidents, st.session_state.events, nodes, links, metrics, generate_demo_incidents)

elif menu == "ACADEMIC SUBJECTS":
    render_academic_subjects()

elif menu == "TRACEABILITY MATRIX":
    render_traceability()

elif menu == "VIVA MODE":
    render_viva()

elif menu == "SYSTEM LOGS":
    def replay_event(saved):
        do_analysis(saved["telemetry"], saved["nodes"], saved["links"])
    def clear_session_logs():
        st.session_state.incidents = []
        st.session_state.events = []
        st.session_state.current = None
        logger.info("session_incident_logs_cleared")
        st.rerun()
    render_system_logs(st.session_state.incidents, st.session_state.events, replay_event, clear_session_logs)

elif menu == "ABOUT PROJECT":
    render_about()
