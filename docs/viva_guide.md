# Viva preparation guide

The dashboard's Viva Mode contains 40+ categorized questions. Each answer includes a short student-friendly response, a technical answer and a code reference. Main preparation points:

1. **Objective:** demonstrate explainable fault detection and topology localization using synthetic telecom measurements.
2. **AI rules:** ordered IF-THEN conditions return every matched candidate with evidence and recommended action.
3. **ML classifier:** a locally trained Random Forest predicts one of eight generated labels and exposes class probabilities.
4. **Anomaly detection:** Isolation Forest reports unusualness; it does not choose a known fault class.
5. **Graph:** towers are vertices, links are edges, and Java stores an adjacency representation.
6. **DFS/BFS:** each is O(V+E) time and O(V) auxiliary space; DFS explores a branch, BFS returns hop-level reachability and shortest unweighted routes.
7. **Multi-fault handling:** simultaneous telemetry can satisfy several rule predicates; the diagnosis retains a primary candidate and separately ranked secondary candidates.
8. **Integration:** Python serializes a topology request to JSON, invokes Java via subprocess, then parses the JSON response.
9. **Resilience:** 50% reachability + 30% active-link availability + 20% alternate-route availability, weighted by their measured ratios.
10. **Prototype boundaries:** synthetic data is not live operator telemetry; holdout ML metrics do not establish production accuracy; maintenance risk is not a validated forecast.

Use the code references shown in each dashboard answer to trace every explanation to the implementation.
