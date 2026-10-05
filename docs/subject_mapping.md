# JNTUK R23 subject-to-code mapping

The dashboard's **ACADEMIC SUBJECTS USED** page provides the detailed what/why/how/file/input/processing/output/benefit/viva view. **TRACEABILITY MATRIX** is the implementation table. Each claim below corresponds to code that runs.

| Subject | Unit/topic | Implementation evidence |
|---|---|---|
| AI | Unit 1: knowledge representation and rule diagnosis | `python_engine/rule_engine.py` contains deterministic IF-THEN symptom predicates and evidence. |
| AI | Unit 2: graph search, DFS and BFS | `java_engine/src/DFS.java`, `BFS.java`, and `Main.java` execute traversal and route analysis. |
| ADSA | Unit 2: graph representation and traversal | `NetworkGraph.java`, `Node.java`, and `Link.java` implement adjacency lists; DFS/BFS are O(V+E) time and O(V) traversal space. |
| OOPJ | classes, constructors, encapsulation and collections | Java domain classes use constructors, private fields, getters, maps/lists/sets/queues and graph validation. |
| OOPJ | exception handling and process I/O | Graph operations throw on invalid inputs; Java stdin/stdout exchanges JSON with Python subprocess. |
| OOPJ | inheritance / polymorphism / interfaces | Not claimed: this graph model has no useful subtype or interface behavior. |
| Python | data preparation and features | `app.py` uses Pandas to read CSV; `classifier.py` uses NumPy for seeded synthetic features. |
| Python | supervised ML and evaluation | `classifier.py` uses Random Forest, stratified train/test split, `predict_proba`, accuracy, macro precision/recall/F1 and a confusion matrix. |
| Python | anomaly detection | `anomaly_detector.py` uses Isolation Forest independently from classification. |
| Python | Streamlit and visualization | `app.py`, `ui/*.py`, NetworkX and Matplotlib display real topology, diagnosis and analytics. |
| Python | simulation, JSON and subprocess | `telemetry_generator.py`, `simulation_engine.py` and `integration/java_bridge.py` implement these workflows. |
| Python | logging and errors | `utils/logger.py` writes rotating JSON-line logs; controller/bridge expose actionable errors. |
