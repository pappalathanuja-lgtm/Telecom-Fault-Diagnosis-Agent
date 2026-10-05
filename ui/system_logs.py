"""Session incident log inspection and replay controls."""
import pandas as pd
import streamlit as st

def render_system_logs(incidents: list[dict], saved_events: list[dict], replay, clear) -> None:
    st.subheader("System Logs · Incident Replay")
    if not incidents:
        st.info("No incident records are stored in this session. Run a simulation to create a replayable diagnosis record.")
        return
    rows = [{"incident_id": e.get("incident_id"), "timestamp": e.get("timestamp"), "event_type": "DIAGNOSIS_COMPLETED", "fault_type": e.get("fault_type"), "severity": e.get("severity"), "affected_tower": e.get("affected_node"), "affected_link": e.get("affected_link"), "confidence": e.get("confidence"), "diagnosis_time_ms": e.get("diagnosis_time_ms")} for e in incidents]
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    # Replay inserts a new session record; render this pass from a snapshot to keep
    # iteration stable and widget keys unique until the next Streamlit rerun.
    for saved in list(saved_events):
        event = saved["incident"]
        with st.expander(f"{event['incident_id']} · {event['fault_type']} · {event['timestamp']}"):
            st.write("Pipeline events: telemetry captured → Java graph analysis → DFS → BFS → rules → ML → anomaly detection → root cause ranking → diagnosis stored.")
            st.json(event)
            st.json({"stored_telemetry": saved["telemetry"], "stored_graph": saved["graph"] if "graph" in saved else event.get("graph_result"), "stored_nodes": saved["nodes"], "stored_links": saved["links"]})
            if st.button("Replay Incident", key=f"replay_{event['incident_id']}"):
                replay(saved)
    st.divider()
    if st.button("Clear Session Logs", help="Clears only incident and replay records held in this browser session; the persistent system.log file is retained."):
        clear()
    st.markdown("#### Structured application log")
    from pathlib import Path
    path = Path(__file__).resolve().parents[1] / "logs" / "system.log"
    if path.exists():
        lines = path.read_text(encoding="utf-8").splitlines()[-200:]
        st.code("\n".join(lines) if lines else "No file log entries yet.")
    else:
        st.info("The persistent application log is created when the first diagnosis or error is recorded.")
