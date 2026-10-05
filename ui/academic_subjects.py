"""Interactive academic topic map tied to concrete source files."""
import streamlit as st

TOPICS = {
    "AI": [
        ("Unit 1", "Rule-Based Diagnostic Agent", "Knowledge representation and IF-THEN inference over measured symptoms.", "python_engine/rule_engine.py", "Telemetry feature dictionary", "Evaluate all configured predicates and score matched rules", "Ranked fault candidates, evidence, severity and actions", "Gives deterministic, inspectable diagnostic evidence", "Rules compare telemetry thresholds and return every matching hypothesis."),
        ("Unit 2", "DFS/BFS Fault-Path Tracing", "State-space graph search using depth-first and breadth-first strategies.", "java_engine/src/DFS.java; java_engine/src/BFS.java; Main.java", "JSON tower/link topology and start tower", "Java DFS recursion and BFS queue traversal", "Visit order, hop levels, reachability and routes", "Localizes topology impact after failures", "DFS explores deeply; BFS visits hop levels; each runs in O(V+E) time."),
    ],
    "ADSA": [
        ("Unit 2", "Graph representation", "Vertices represent towers and edges represent links, stored in adjacency lists.", "java_engine/src/NetworkGraph.java; Node.java; Link.java", "Tower IDs and link endpoints", "Build indexed vertices and incident-link collections", "Traversable network graph", "Models the topology directly", "Adjacency lists support O(V+E) graph traversals."),
        ("Unit 2", "DFS, BFS and shortest path", "DFS explores a branch; BFS explores level by level and finds shortest unweighted routes.", "java_engine/src/DFS.java; BFS.java; Main.java", "Graph, source and optional destination", "Visited sets, recursion, queue and predecessor map", "Traversal, hop levels, route and unreachable nodes", "Shows path impact and possible detours", "Both take O(V+E) time and O(V) auxiliary space."),
    ],
    "OOPJ": [
        ("—", "Classes, objects, constructors, encapsulation", "Node, Link, Fault, FaultPath and NetworkGraph model domain entities with private fields and constructors.", "java_engine/src/Node.java; Link.java; Fault.java; FaultPath.java; NetworkGraph.java", "Tower and link fields", "Create objects, connect links, expose controlled getters", "Validated graph objects", "Keeps network logic modular", "Node and Link constructors create objects; private fields and getters provide encapsulation."),
        ("—", "Collections and exceptions", "Maps, lists, sets and queues store topology and traversal state; invalid graph operations throw errors.", "java_engine/src/NetworkGraph.java; DFS.java; BFS.java", "Graph update and traversal requests", "Validate IDs and maintain graph collections", "Graph result or explicit exception", "Prevents silent graph corruption", "The graph uses Java collections and IllegalArgumentException for invalid references."),
        ("—", "Inheritance, polymorphism and interfaces", "These require useful subtype or interface behavior; the current graph engine has no such use case.", "Not claimed; no implementation file", "—", "Not used", "—", "Avoids artificial OOP claims", "I did not add inheritance or polymorphism because they do not improve this model."),
        ("—", "JSON process I/O", "Java reads graph JSON from stdin and returns JSON on stdout.", "java_engine/src/Main.java; integration/java_bridge.py", "Python-serialized topology JSON", "Run Java CLI, parse the request and serialize traversal result", "Graph analysis JSON", "Provides real Python–Java integration", "Python invokes Java with subprocess and exchanges JSON through standard streams."),
    ],
    "PYTHON": [
        ("—", "Data processing, modules and file I/O", "Python functions and packages process dictionaries/lists; Pandas reads topology CSV.", "app.py; python_engine/*.py", "CSV topology and telemetry records", "Load, validate and assemble named model features", "Structured records and model-ready features", "Separates data preparation from UI", "Pandas loads synthetic nodes and links; Python modules pass telemetry dictionaries."),
        ("—", "Random Forest classification and evaluation", "A supervised ensemble predicts one of eight generated fault labels.", "python_engine/classifier.py", "Synthetic numeric features and labels", "Stratified split, fit, predict_proba, metric evaluation", "Probabilities, accuracy, macro precision/recall/F1 and confusion matrix", "Adds a measurable learned classifier", "The model is trained on synthetic samples; its scores are not production performance."),
        ("—", "Anomaly detection", "Isolation Forest identifies unusual telemetry without naming a fault class.", "python_engine/anomaly_detector.py", "Telemetry vector", "Outlier score and label", "NORMAL/SUSPICIOUS/ANOMALOUS", "Separates unusualness from classification", "The classifier predicts a known label; Isolation Forest scores atypical patterns."),
        ("—", "Streamlit, JSON, subprocess and exceptions", "Streamlit renders operations pages; subprocess and JSON connect to Java.", "app.py; ui/*.py; integration/java_bridge.py", "Scenario input and graph data", "Render UI, serialize JSON, invoke Java, catch integration errors", "Interactive diagnosis and graph results", "Runs the complete local workflow", "Python orchestrates the dashboard and Java traversal through JSON."),
    ],
}

def render_academic_subjects() -> None:
    st.subheader("ACADEMIC SUBJECTS USED")
    subject = st.radio("Select subject", list(TOPICS), horizontal=True)
    for unit, topic, what, files, input_, processing, output, benefit, viva in TOPICS[subject]:
        with st.expander(f"{unit} · {topic}", expanded=True):
            fields = [("WHAT IS IT?", what), ("WHY IS IT USED?", f"It supports {subject} learning outcomes and the network diagnosis workflow."), ("HOW IS IT USED?", processing), ("IMPLEMENTATION FILE", files), ("INPUT", input_), ("PROCESSING", processing), ("OUTPUT", output), ("PROJECT BENEFIT", benefit), ("VIVA EXPLANATION", viva)]
            for label, value in fields:
                st.markdown(f"**{label}**  \n{value}")
