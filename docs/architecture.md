# Architecture and data flow

The official project title is **Telecom Fault Diagnosis Agent**. **TeleGuard AI** is the product branding. Streamlit in `app.py` handles navigation and delegates pages to `ui/`; domain logic lives in `python_engine/`.

## Diagnosis flow

1. `data/network_nodes.csv` and `data/network_links.csv` provide a repeatable synthetic baseline.
2. `python_engine/simulation_engine.py` or `telemetry_generator.py` creates fault symptoms and time-stamped samples.
3. `rule_engine.py` applies every matching IF-THEN rule; `classifier.py` produces a Random Forest class probability; `anomaly_detector.py` reports outlier status separately.
4. `diagnosis.py` combines rule score, ML probability and anomaly weight, chooses a graph start from the fault location/link, and returns ranked primary/secondary candidates with evidence and actions.
5. `integration/java_bridge.py` serializes nodes and links as JSON, compiles changed Java sources, invokes the Java CLI with a timeout and parses the output.
6. `NetworkGraph` stores adjacency lists. Java DFS returns exploration order, BFS returns levels/reachability, and the Java route method reconstructs the shortest healthy-link path.
7. The result stores telemetry, all candidates, graph output, model output, anomaly result, root-cause candidate and action in session state for analytics and replay.

## Graph algorithms

With V towers and E links, adjacency-list DFS and BFS each take O(V+E) time and O(V) auxiliary traversal space. Java BFS also computes an unweighted shortest route using a predecessor map. Link failures remove that edge from the reachable graph; tower and power outages mark incident links down.

## Resilience

`python_engine/resilience.py` computes `100 × (0.50 × reachable tower ratio + 0.30 × available link ratio + 0.20 × alternate route availability)`. The UI shows each weighted contribution and an interpretation label. This score is a simple scenario indicator, not a telecom service-level guarantee.

## Model and risk boundaries

Random Forest holdout metrics are calculated from generated labelled examples. Isolation Forest detects unusual patterns but does not assign known fault labels. Predictive maintenance averages normalized temperature, CPU, error, loss, latency, signal and repeated-anomaly indicators. These results are explicitly prototypes using synthetic telemetry.

## Persistence

Incident/replay records persist for the active Streamlit browser session. `utils/logger.py` writes rotating JSON-line operational logs locally; clearing session incidents does not delete the log file. No cloud API or telecom network is called.
