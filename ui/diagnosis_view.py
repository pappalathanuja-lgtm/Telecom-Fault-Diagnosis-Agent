"""Diagnosis result and user-facing evidence presentation."""
import pandas as pd
import streamlit as st

def render_diagnosis(current: dict | None) -> None:
    if not current:
        st.info("No diagnosis yet. Run a fault injection or telemetry analysis to begin.")
        return
    event = current["event"]
    a, b, c = st.columns(3)
    a.metric("PRIMARY DIAGNOSIS", event["fault_type"])
    b.metric("CONFIDENCE", f"{event['confidence']:.0%}")
    c.metric("SEVERITY", event["severity"])
    st.write(f"**Incident:** {event['incident_id']} · **Root-cause candidate:** {event['root_cause']} · **Time:** {event['timestamp']}")
    if event.get("secondary_faults"):
        st.markdown("#### Secondary fault candidates")
        st.dataframe(pd.DataFrame(event["secondary_faults"]), hide_index=True, width="stretch")
    with st.expander("Ranked fault candidates"):
        st.dataframe(pd.DataFrame(event.get("ranked_candidates", [])), hide_index=True, width="stretch")
    st.markdown("#### Measured evidence")
    for group, evidence in event["evidence"].items():
        with st.expander(group.upper()): st.json(evidence)
    st.write("**Recommended action:** " + event["recommended_action"])
    if len(event.get("recommended_actions", [])) > 1:
        st.write("**Additional actions:** " + " · ".join(event["recommended_actions"][1:]))
    st.caption(f"Java traversal time {event['diagnosis_time_ms']} ms · model {event['model_version']}")
