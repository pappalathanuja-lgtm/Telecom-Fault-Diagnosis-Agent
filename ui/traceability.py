"""Traceability rows link taught concepts to implemented code."""
import pandas as pd
import streamlit as st

ROWS = [
 ("AI","Unit 1","IF-THEN production rules","python_engine/rule_engine.py","Rule predicates","Telemetry features","Matching fault hypotheses","Symptom inference","Rules encode readable IF condition THEN fault evidence."),
 ("AI","Unit 1","Evidence and confidence ranking","python_engine/diagnosis.py","Rule/ML score fusion","Rule scores and class probabilities","Ranked diagnosis candidates","Evidence combination","Candidate confidence combines rule strength and classifier probability."),
 ("AI","Unit 2","Depth-first search","java_engine/src/DFS.java","DFS","Graph + start tower","Visit order","Fault-path exploration","Recursively explores each healthy-link branch."),
 ("AI","Unit 2","Breadth-first search","java_engine/src/BFS.java","BFS","Graph + start tower","Hop levels and visited set","Impact localization","Queue traversal groups towers by hop depth."),
 ("ADSA","Unit 2","Graph representation","java_engine/src/NetworkGraph.java; Node.java; Link.java","Adjacency lists","Tower/link JSON","Java network graph","Topology model","Vertices are towers; edges are communication links."),
 ("ADSA","Unit 2","Shortest route / reachability","java_engine/src/Main.java","BFS predecessor path","Source, destination, healthy links","Shortest route or unreachable","Alternative routing","Shortest unweighted route returned by Java."),
 ("OOPJ","—","Classes, objects, constructors","java_engine/src/Node.java; Link.java; Fault.java","Java classes","Domain attributes","Graph objects","Encapsulation","Constructors establish node/link/fault object state."),
 ("OOPJ","—","Encapsulation","java_engine/src/Node.java; Link.java","Private fields/getters","IDs, endpoints, status","Controlled state access","Data integrity","Fields are private with public accessor methods."),
 ("OOPJ","—","Collections and exception handling","java_engine/src/NetworkGraph.java; BFS.java","Map/List/Set/Queue","Graph operations","Traversal or explicit error","Reliable operations","Unknown nodes and invalid links raise exceptions."),
 ("OOPJ","—","JSON process I/O","java_engine/src/Main.java; integration/java_bridge.py","stdin/stdout + subprocess","Graph request JSON","Graph response JSON","Cross-language integration","Python calls Java CLI and parses its JSON result."),
 ("Python","—","Pandas topology loading","app.py","Pandas CSV","network_nodes.csv/network_links.csv","DataFrames and records","Data preparation","CSV is loaded with relative project paths."),
 ("Python","—","NumPy feature generation","python_engine/classifier.py","Synthetic generation","Seeded fault profiles","Numeric feature matrix","Reproducible training data","Each generated label has distinguishable numeric ranges."),
 ("Python","—","Random Forest and split","python_engine/classifier.py","RandomForestClassifier/train_test_split","Labelled synthetic samples","Trained fault classifier","ML classification","Stratified holdout prevents class imbalance in evaluation."),
 ("Python","—","Model evaluation","python_engine/classifier.py","sklearn metrics","Holdout labels/predictions","Accuracy, macro P/R/F1, matrix","Performance reporting","Metrics describe generated data only."),
 ("Python","—","Isolation Forest","python_engine/anomaly_detector.py","IsolationForest","Telemetry features","Anomaly score/status","Outlier detection","Anomaly detection is distinct from fault classification."),
 ("Python","—","Telemetry simulation","python_engine/telemetry_generator.py; ui/realtime.py","Stateful seeded generator + Streamlit fragment","Tower ID and simulation state","Time-stamped telemetry samples","Realtime demonstration","Fragment refreshes without a blocking loop."),
 ("Python","—","Route/resilience analysis","python_engine/route_analysis.py; python_engine/resilience.py","Java shortest path + weighted formula","Baseline/failure graphs","Route comparison and resilience breakdown","What-if analysis","The formula weights reachability 0.50, link availability 0.30 and detour availability 0.20."),
 ("Python","—","Predictive maintenance prototype","python_engine/predictive_engine.py","Normalized synthetic indicators","Telemetry history","Tower risk/factors/action","Maintenance demonstration","Risk is a transparent prototype, not a production forecast."),
 ("Python","—","Streamlit charts and pages","app.py; ui/*.py","Streamlit/pandas","Session state and model metrics","NOC/academic/analytics pages","User-facing explanation","Pages display real model/incident values and empty-state actions."),
 ("Python","—","Structured logging and errors","utils/logger.py; app.py","Rotating log + exception handling","Pipeline events","Local structured log records","Operations and diagnosis history","Incidents can be replayed from session records; file logs are separate."),
]

def render_traceability() -> None:
    st.subheader("Subject-to-Code Traceability Matrix")
    st.dataframe(pd.DataFrame(ROWS, columns=["Subject", "Unit", "Topic", "Implementation File", "Algorithm/Technology", "Input", "Output", "Purpose", "Viva Point"]), hide_index=True, width="stretch")
