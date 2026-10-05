# Telecom Fault Diagnosis Agent

**TeleGuard AI** · Intelligent Network Fault Localization & Diagnosis System

A local academic Network Operations Center prototype. Python orchestrates simulated telemetry, deterministic rules, a scikit-learn fault classifier, anomaly scoring and Streamlit pages. Java represents the telecom topology and runs DFS, BFS and shortest-hop route search. The project uses synthetic telemetry because no real operator network is connected.

## Features

- NOC home, tower and link inspection, network topology and session incident history.
- Single or simultaneous fault injection, with ranked primary and secondary candidates.
- Streamlit-fragment simulated telemetry with start/stop, interval and manual sample controls.
- Java graph traversal, reachability, route-before/after comparison and what-if scenarios.
- Explainable resilience formula and contribution breakdown.
- Analytics with actual session incident counts, classifier metrics, anomaly counts and timeline; the empty state can generate incidents through the actual pipeline.
- Prototype maintenance risk from synthetic tower telemetry, with factors and suggested action.
- Replayable session incident records and rotating JSON-line logs.
- Interactive AI, ADSA, OOPJ and Python mapping, traceability matrix, and 40+ viva questions.

## Local setup

Install Python 3.10+ and JDK 17+; ensure both `java` and `javac` are on `PATH`. Then, in PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
java -version
javac -version
streamlit run app.py
```

The Python–Java bridge compiles sources to `java_engine/out` on first graph request or after a Java source change. No API key, telecom hardware or external runtime service is needed. Python paths are relative to the project; the application does not depend on a user-specific absolute path.

If PowerShell blocks virtual-environment activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.

## Java graph JSON contract

The CLI reads one JSON object from stdin, containing `nodes` with `tower_id`, `links` with `link_id`, `source`, `destination`, `status`, plus `start` and optionally `destination`. It emits `dfs_path`, `bfs_levels`, visited/affected nodes and links, timing, and an optional shortest `route_path` as JSON on stdout. The Python bridge handles compilation, process timeouts and errors.

## Tests

```powershell
python -m unittest discover -s tests -v
```

Coverage includes normal and fault rules, multi-fault ranking, classifier probabilities and metrics, anomaly output, telemetry sampling, Java DFS/BFS and route search, resilience, predictive maintenance, topology scenarios and Streamlit page/workflow smoke checks.

## Deployment

For Streamlit Community Cloud, use `app.py` as the entry point. `requirements.txt` installs Python dependencies and `packages.txt` requests OpenJDK 17 JDK so the Java bridge can compile and execute the graph engine. Commit `java_engine/src/`; compiled output, `.venv` and runtime logs are ignored.

## Academic mapping

See **ACADEMIC SUBJECTS USED**, **TRACEABILITY MATRIX**, and `docs/subject_mapping.md`. DFS/BFS each run in O(V+E) time and O(V) auxiliary space. Inheritance and polymorphism are not claimed because the graph engine has no useful subtype behavior.

## Screenshots

Add presentation screenshots here after capturing the local dashboard pages.

## Limitations and future scope

Training/evaluation data and network measurements are synthetic; the generated model metrics are not production accuracy claims. Root-cause ranking is evidence-based but uncertain. Maintenance scoring is a transparent prototype based on normalized signals, not a validated failure forecast. Future scope includes approved real telemetry, validated site-specific thresholds, weighted routing, persistent incident storage and production security controls.
