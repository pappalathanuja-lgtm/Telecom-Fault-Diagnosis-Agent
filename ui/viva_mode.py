"""Student-friendly and technical viva preparation questions."""
import streamlit as st

QUESTIONS = {
"Project Overview": [
 ("What is the main objective?","Diagnose and localize simulated telecom faults faster.","The system fuses telemetry rules, ML probabilities and Java graph reachability.","app.py; python_engine/diagnosis.py"),
 ("Why is the project useful to a NOC?","It organizes symptoms and affected network paths.","It demonstrates evidence-backed fault triage and topology impact analysis.","app.py; java_engine/src/Main.java"),
 ("What is synthetic data?","Generated data that imitates plausible telemetry.","Seeded profiles provide labels and threshold patterns without carrier access.","python_engine/classifier.py; data/*.csv"),
 ("What are the key limitations?","It is a small simulated prototype.","No live carrier data, production validation, or calibrated operational threshold set is provided.","README.md; docs/architecture.md"),
],
"AI": [
 ("What is a production rule?","A condition followed by an action or conclusion.","An IF predicate tests a telemetry threshold and emits a fault hypothesis with evidence.","python_engine/rule_engine.py"),
 ("What is knowledge representation here?","The rules encode symptom-to-fault knowledge.","Predicates and human-readable evidence represent domain thresholds explicitly.","python_engine/rule_engine.py"),
 ("How is confidence calculated?","Rule strength and model probability are combined.","The candidate score uses 0.65 times rule score plus 0.35 times class probability.","python_engine/diagnosis.py"),
 ("What is root-cause analysis?","Finding a likely source behind symptoms.","This prototype ranks fault candidates and uses the selected node/link plus graph reachability as evidence.","python_engine/diagnosis.py"),
],
"ADSA": [
 ("Why represent the network as a graph?","Towers connect through links.","Towers are vertices; links are edges in adjacency lists.","java_engine/src/NetworkGraph.java"),
 ("Why did you use DFS?","To explore the affected connectivity region.","DFS recursively visits healthy-link neighbors and records exploration order.","java_engine/src/DFS.java"),
 ("Why did you use BFS?","To see reachable towers by hop level.","BFS uses a queue, returns levels and supports shortest unweighted route.","java_engine/src/BFS.java; Main.java"),
 ("What is DFS time complexity?","O(V+E).","Each vertex and adjacency edge is visited at most a constant number of times.","java_engine/src/DFS.java"),
 ("What is BFS time complexity?","O(V+E).","Adjacency-list BFS processes each vertex and edge once.","java_engine/src/BFS.java"),
 ("What is the traversal space complexity?","O(V).","Visited collections, recursion depth or queue and predecessor map scale with vertices.","java_engine/src/DFS.java; BFS.java; Main.java"),
],
"OOPJ": [
 ("Name Java classes in the project.","Node, Link, Fault, FaultPath, NetworkGraph, DFS and BFS.","They model domain entities and isolate graph behavior.","java_engine/src/*.java"),
 ("Where is encapsulation used?","Node and Link keep fields private.","Public getters and graph methods control access to internal state.","java_engine/src/Node.java; Link.java"),
 ("Is inheritance used?","No.","There is no useful subtype relationship in this graph model, so it is not claimed.","Academic Subjects page"),
 ("Which Java collections are used?","Maps, lists, sets and queues.","They index vertices, store adjacency and track traversal state.","java_engine/src/NetworkGraph.java; BFS.java"),
],
"Python": [
 ("How is Python organized?","Into modules for models, rules, simulation and UI pages.","The app orchestrates reusable functions from python_engine, integration and ui packages.","app.py; python_engine/; ui/"),
 ("How is telemetry loaded?","Pandas reads the local CSV topology.","Relative paths from app.py locate node and link CSVs.","app.py"),
 ("How are exceptions handled?","The bridge and UI report Java and diagnosis errors.","Subprocess failures are raised with diagnostic context and caught at the presentation boundary.","integration/java_bridge.py; app.py"),
 ("How are lists and dictionaries used?","They carry nodes, links, features and incidents.","Each telemetry sample is a keyed record and topology is a list of records.","python_engine/*.py"),
],
"ML": [
 ("Why use Random Forest?","It handles tabular features and multiple fault labels.","A seeded ensemble provides class probability output for the demonstration.","python_engine/classifier.py"),
 ("Why use a train/test split?","To evaluate on held-out samples.","A stratified split preserves class proportions between training and holdout partitions.","python_engine/classifier.py"),
 ("What is precision?","How many predicted positives are correct.","TP/(TP+FP), averaged by class in the displayed macro metric.","python_engine/classifier.py"),
 ("What is recall?","How many actual positives were found.","TP/(TP+FN), macro-averaged across generated labels.","python_engine/classifier.py"),
 ("What is F1?","A balance between precision and recall.","The harmonic mean 2PR/(P+R), macro-averaged for class-balanced reporting.","python_engine/classifier.py"),
 ("What does the confusion matrix show?","Actual versus predicted fault labels.","Rows are actual classes and columns are predictions in the displayed ordering.","ui/analytics.py"),
 ("How does anomaly detection differ from classification?","It flags unusualness instead of naming a known fault.","Isolation Forest outlier score is independent of the Random Forest class probabilities.","python_engine/anomaly_detector.py"),
],
"Java Integration": [
 ("How does Python communicate with Java?","Through a local command-line process and JSON.","Python serializes stdin, invokes javac/java with subprocess, and parses stdout JSON.","integration/java_bridge.py; java_engine/src/Main.java"),
 ("What happens if Java is missing?","The UI shows a setup error.","The bridge checks javac/java on PATH and raises JavaUnavailable with installation guidance.","integration/java_bridge.py"),
 ("Why compile on demand?","It simplifies local setup.","The bridge compiles Java sources to java_engine/out before execution.","integration/java_bridge.py"),
],
"Streamlit": [
 ("What does Streamlit provide?","The local interactive dashboard.","Sidebar navigation, stateful inputs, metrics, tables, charts and fragment refresh.","app.py; ui/*.py"),
 ("Why use session state?","To retain incidents and running simulation state across reruns.","Streamlit reruns scripts per interaction, so mutable workflow state is stored in session_state.","app.py; ui/realtime.py"),
],
"Network Simulation": [
 ("How are faults simulated?","Telemetry and link state are changed from a baseline.","Fault profiles update selected symptoms and graph link statuses before analysis.","python_engine/simulation_engine.py; what_if.py"),
 ("How is an alternative route found?","Java BFS finds a healthy-link route.","A predecessor map reconstructs the shortest unweighted route after failure.","java_engine/src/Main.java; python_engine/route_analysis.py"),
 ("How is resilience calculated?","From reachable towers, available links and a detour route.","The visible weighted score is 50% reachability, 30% link availability, 20% route availability.","python_engine/resilience.py"),
 ("What does simulated real time mean?","The app generates periodic local samples.","A Streamlit fragment refreshes on a timer without a blocking loop or hardware connection.","python_engine/telemetry_generator.py; ui/realtime.py"),
],
"Testing": [
 ("What tests cover the project?","Unit tests exercise the Python pipeline and Java graph behavior.","Unittest suites cover rules, classifier, anomaly, simulation, routes, resilience, replay and bridge; direct Java cases validate DFS/BFS.","tests/"),
 ("How are integration errors reported?","With useful UI messages and local structured logs.","The bridge raises on compile, timeout and process errors; UI logs stack context.","integration/java_bridge.py; utils/logger.py"),
],
"Future Scope": [
 ("How could the model improve?","Train it on approved real operator data.","Validate calibrated thresholds and model drift across sites and time windows.","docs/architecture.md"),
 ("What is a future feature?","Add operator integrations and broader route planning.","Production work would require secure telemetry connectors, authentication, audit and domain validation.","docs/viva_guide.md"),
]
}

def render_viva() -> None:
    st.subheader("Viva Mode · Questions and answers")
    st.caption(f"{sum(map(len, QUESTIONS.values()))} questions · student-friendly and technical answers")
    category = st.selectbox("Category", list(QUESTIONS))
    for index, (question, short, technical, reference) in enumerate(QUESTIONS[category], 1):
        with st.expander(f"{index}. {question}"):
            st.markdown(f"**Short answer**  \n{short}")
            st.markdown(f"**Technical answer**  \n{technical}")
            st.markdown(f"**Project reference**  \n`{reference}`")
