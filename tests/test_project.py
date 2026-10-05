"""Unit and local integration coverage for diagnosis and graph workflows."""
from __future__ import annotations

import unittest
from pathlib import Path
import pandas as pd

from integration.java_bridge import run_graph
from python_engine.anomaly_detector import detect, train_detector
from python_engine.classifier import classify, train_model
from python_engine.diagnosis import analyze
from python_engine.predictive_engine import predict_maintenance
from python_engine.resilience import calculate_resilience
from python_engine.route_analysis import analyze_routes
from python_engine.rule_engine import diagnose
from python_engine.simulation_engine import BASE_TELEMETRY, inject_multiple
from python_engine.telemetry_generator import TelemetryGenerator
from python_engine.what_if import simulate

ROOT = Path(__file__).resolve().parents[1]

def topology():
    nodes = pd.read_csv(ROOT / "data" / "network_nodes.csv").to_dict("records")
    links = pd.read_csv(ROOT / "data" / "network_links.csv").to_dict("records")
    return nodes, links


class RuleTests(unittest.TestCase):
    def test_normal_and_faults(self):
        self.assertEqual(diagnose(BASE_TELEMETRY)[0]["fault_type"], "Normal")
        cases = {
            "Tower Power Failure": {**BASE_TELEMETRY, "power_ok": 0},
            "Fiber Link Failure": {**BASE_TELEMETRY, "link_down": 1},
            "Hardware Failure": {**BASE_TELEMETRY, "temperature": 92},
            "Signal Degradation": {**BASE_TELEMETRY, "signal_strength": .2},
            "Network Congestion": {**BASE_TELEMETRY, "cpu_load": .95, "latency_ms": 120},
            "High Latency": {**BASE_TELEMETRY, "latency_ms": 150},
            "Packet Loss": {**BASE_TELEMETRY, "packet_loss": 30},
        }
        for expected, symptoms in cases.items():
            with self.subTest(expected=expected):
                self.assertIn(expected, [item["fault_type"] for item in diagnose(symptoms)])

    def test_multiple_matching_rules_are_returned(self):
        result = diagnose({**BASE_TELEMETRY, "latency_ms": 160, "packet_loss": 40, "signal_strength": .2, "cpu_load": .95})
        names = {item["fault_type"] for item in result}
        self.assertTrue({"High Latency", "Packet Loss", "Signal Degradation", "Network Congestion"}.issubset(names))


class MLTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model, cls.metrics = train_model()
        cls.anomaly = train_detector()

    def test_classifier_outputs_probability_and_evaluation(self):
        result = classify(self.model, {**BASE_TELEMETRY, "link_down": 1, "latency_ms": 180, "packet_loss": 90})
        self.assertIn(result["fault_type"], self.model.classes_)
        self.assertGreaterEqual(result["confidence"], 0)
        self.assertAlmostEqual(sum(result["probabilities"].values()), 1.0, places=5)
        for key in ("accuracy", "precision_macro", "recall_macro", "f1_macro", "matrix"):
            self.assertIn(key, self.metrics)

    def test_anomaly_separate_status(self):
        result = detect(self.anomaly, {**BASE_TELEMETRY, "temperature": 110, "cpu_load": 1})
        self.assertIn(result["status"], {"NORMAL", "SUSPICIOUS", "ANOMALOUS"})
        self.assertIn("score", result)


class SimulationTests(unittest.TestCase):
    def test_realtime_samples_are_timestamped_and_progress(self):
        generator = TelemetryGenerator(seed=7)
        first, second = generator.next_sample("T01", "NORMAL"), generator.next_sample("T01", "FAULT")
        self.assertIn("timestamp", first)
        self.assertEqual(second["connectivity_status"], "DEGRADED")
        self.assertEqual(second["failed_link"], "L05")
        self.assertGreaterEqual(generator.sample_number, 2)

    def test_composed_fault_profiles_keep_simultaneous_evidence(self):
        nodes, links = topology()
        telemetry, _, changed_links = inject_multiple(["High Latency", "Signal Degradation", "Network Congestion"], "T03", "L02", nodes, links)
        self.assertEqual(telemetry["latency_ms"], 115)
        self.assertEqual(telemetry["signal_strength"], .22)
        self.assertEqual(telemetry["cpu_load"], .94)
        self.assertTrue(all(link["status"] == "UP" for link in changed_links))


class GraphAndDiagnosisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model, _ = train_model()
        cls.anomaly = train_detector()
        cls.nodes, cls.links = topology()

    def test_java_dfs_bfs_and_shortest_route(self):
        edges = [dict(link) for link in self.links]
        edges[0]["status"] = "DOWN"
        result = run_graph({"nodes": self.nodes, "links": edges, "start": "T01", "destination": "T02"})
        self.assertIn("T01", result["dfs_path"])
        self.assertTrue(result["bfs_levels"])
        self.assertTrue(result["route_path"])
        self.assertIn("L01", result["affected_links"])

    def test_route_before_and_after_failure_uses_java_paths(self):
        failed = [dict(link) for link in self.links]
        failed[0]["status"] = "DOWN"
        result = analyze_routes(self.nodes, self.links, failed, "T01", "T02", run_graph)
        self.assertEqual(result["primary_route"], ["T01", "T02"])
        self.assertTrue(result["available"])
        self.assertGreater(result["alternative_hops"], 1)
        self.assertEqual(result["affected_links"], ["L01"])

    def test_resilience_is_explainable_and_bounded(self):
        graph = run_graph({"nodes": self.nodes, "links": self.links, "start": "T01"})
        result = calculate_resilience(graph, self.nodes, self.links, True)
        self.assertEqual(result["score"], 100)
        self.assertIn("reachable tower ratio", result["formula"])
        partial = calculate_resilience({"visited_nodes": ["T01"]}, self.nodes, self.links[:-1], False)
        self.assertLess(partial["score"], 100)

    def test_diagnosis_ranks_multifault_candidates_and_replays_fields(self):
        telemetry = {**BASE_TELEMETRY, "latency_ms": 140, "packet_loss": 32, "signal_strength": .2, "cpu_load": .95, "affected_node": "T07"}
        event, rules, ml, anomaly, graph = analyze(telemetry, self.nodes, self.links, self.model, self.anomaly, run_graph)
        self.assertIn("primary_fault", event)
        self.assertGreaterEqual(len(event["secondary_faults"]), 2)
        self.assertIn("graph_result", event)
        self.assertIn("telemetry", event)
        self.assertIn("recommended_actions", event)

    def test_tower_outage_and_predictive_maintenance(self):
        nodes, links, telemetry = simulate("Power Failure", ["T05"], [], self.nodes, self.links)
        self.assertTrue(any(edge["status"] == "DOWN" for edge in links))
        risk = predict_maintenance("T05", [{"tower_id": "T05", **telemetry, "temperature": 95, "cpu_load": .98}])
        self.assertIn(risk["category"], {"LOW", "MEDIUM", "HIGH"})
        self.assertIn("factors", risk)


if __name__ == "__main__":
    unittest.main()
