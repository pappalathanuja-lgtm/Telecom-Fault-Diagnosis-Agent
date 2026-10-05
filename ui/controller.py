"""Session-bound diagnosis orchestration, storage and error reporting."""
import streamlit as st
from python_engine.diagnosis import analyze
from integration.java_bridge import JavaUnavailable

def make_analysis_handler(model, anomaly_model, graph_fn, logger):
    def do_analysis(telemetry, nodes, links):
        try:
            event, rules, ml, anomaly, graph = analyze(telemetry, nodes, links, model, anomaly_model, graph_fn)
            st.session_state.current = {"event":event,"rules":rules,"ml":ml,"anomaly":anomaly,"graph":graph,"telemetry":telemetry}
            st.session_state.incidents.insert(0, event)
            st.session_state.events.insert(0, {"incident":event,"telemetry":telemetry,"nodes":nodes,"links":links,"graph":graph})
            logger.info("diagnosis_complete incident=%s fault=%s confidence=%.3f", event["incident_id"], event["fault_type"], event["confidence"])
            return True
        except JavaUnavailable as exc:
            logger.error("java_unavailable: %s", exc)
            st.error(str(exc))
            return False
        except Exception as exc:
            logger.exception("diagnosis_failed")
            st.error(f"Diagnosis could not complete: {exc}")
            return False
    return do_analysis
