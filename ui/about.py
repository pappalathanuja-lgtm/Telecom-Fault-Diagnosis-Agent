"""Project overview and honest scope description."""
import streamlit as st

def render_about() -> None:
    st.subheader("About the Project")
    st.markdown("### Telecom Fault Diagnosis Agent")
    st.markdown("**TeleGuard AI** · Intelligent Network Fault Localization & Diagnosis System")
    st.markdown("#### Problem statement")
    st.write("A Network Operations Center needs to locate likely telecom faults faster than manual log checking. This academic prototype combines symptoms, graph connectivity and measured model output to demonstrate a traceable local diagnosis workflow.")
    st.markdown("#### Objective and key features")
    st.write("Model a telecom network as towers and links; simulate telemetry; diagnose with deterministic rules, Random Forest classification and Isolation Forest anomaly detection; run Java DFS/BFS; compare routes; replay incidents; explain evidence and map code to academic subjects.")
    st.markdown("#### Architecture")
    st.code("Synthetic topology/telemetry → Python feature processing → rule + ML + anomaly evidence → JSON subprocess bridge → Java graph, DFS/BFS and shortest route → ranked diagnosis → Streamlit NOC")
    st.markdown("#### Technologies and subjects")
    st.write("Python, Streamlit, Pandas, NumPy, scikit-learn, NetworkX for visualization, Java collections and OOP, JSON and subprocess integration. Demonstrated subjects: AI, ADSA, OOPJ and Python.")
    st.markdown("#### AI/ML and simulation")
    st.write("Rules provide inspectable symptom evidence. Random Forest returns synthetic-label probabilities and holdout metrics. Isolation Forest reports unusualness independently. The local telemetry and fault-injection flows do not require telecom devices.")
    st.markdown("#### Testing")
    st.write("The repository test suite covers rule, classifier, anomaly, diagnosis, graph, Java bridge, real-time sample generation, multi-fault ranking, route and resilience behavior. Run it with `python -m unittest discover -s tests -v`.")
    st.markdown("#### Limitations and future scope")
    st.warning("Topology, historical telemetry and incidents are synthetic. Model metrics are not production accuracy; maintenance risk is a prototype heuristic. No real telecom network is connected.")
    st.write("Future work could validate on authorized operator data, add secure telemetry adapters, calibrate site-specific thresholds and extend weighted routing and persistence.")
    st.caption("Student/team details are intentionally omitted; no names were provided.")
