"""Network topology renderer used by the Home, NOC and scenario pages."""
import streamlit as st

def render_topology(nodes: list[dict], edges: list[dict], focus: str | None = None) -> None:
    try:
        import matplotlib.pyplot as plt
        import networkx as nx
        graph = nx.Graph()
        graph.add_nodes_from(node["tower_id"] for node in nodes)
        for edge in edges:
            graph.add_edge(edge["source"], edge["destination"], status=edge["status"], id=edge["link_id"])
        pos = nx.circular_layout(graph)
        fig, ax = plt.subplots(figsize=(9, 5), facecolor="#08111f")
        ax.set_facecolor("#08111f")
        normal = [node for node in graph if node != focus]
        nx.draw_networkx_nodes(graph, pos, nodelist=normal, node_color="#137d8b", node_size=900, ax=ax)
        if focus in graph:
            nx.draw_networkx_nodes(graph, pos, nodelist=[focus], node_color="#e99d42", node_size=1080, ax=ax)
        nx.draw_networkx_labels(graph, pos, font_color="white", font_size=9, ax=ax)
        healthy = [(a, b) for a, b, data in graph.edges(data=True) if data["status"] == "UP"]
        failed = [(a, b) for a, b, data in graph.edges(data=True) if data["status"] != "UP"]
        nx.draw_networkx_edges(graph, pos, edgelist=healthy, width=2, edge_color="#3d7588", ax=ax)
        nx.draw_networkx_edges(graph, pos, edgelist=failed, width=3, edge_color="#e65757", style="dashed", ax=ax)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels={(a, b): data["id"] for a, b, data in graph.edges(data=True)}, font_size=7, font_color="#b7c5d6", ax=ax)
        ax.axis("off")
        st.pyplot(fig, width="stretch")
        plt.close(fig)
    except Exception as exc:
        st.error(f"Topology rendering failed: {exc}")
