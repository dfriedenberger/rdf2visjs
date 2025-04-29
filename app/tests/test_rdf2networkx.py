from rdflib import Graph
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
from rdf2vis.networkx_utils import rdf2networkx


def test_rdf2networkx():

    # Test with a sample RDF file
    ttl_file = "data/flexidug.ttl"

    g = Graph()
    g.parse(ttl_file, format="turtle")

    graph = rdf2networkx(g)

    # Check if the graph is not empty
    assert len(graph.nodes) > 0, "Graph should not be empty"
    assert len(graph.edges) > 0, "Graph should have edges"

    # Check if the graph has the expected number of nodes and edges
    expected_nodes = 636  # Replace with the expected number of nodes
    expected_edges = 1285  # Replace with the expected number of edges
    assert len(graph.nodes) == expected_nodes, f"Expected {expected_nodes} nodes, got {len(graph.nodes)}"
    assert len(graph.edges) == expected_edges, f"Expected {expected_edges} edges, got {len(graph.edges)}"


def test_hits():
    # Test with a sample RDF file
    ttl_file = "data/flexidug.ttl"

    g = Graph()
    g.parse(ttl_file, format="turtle")

    graph = rdf2networkx(g)
    # HITS-Algorithmus ausführen
    hubs, authorities = nx.hits(graph)

    print("Hub-Werte:")
    sorted_hubs = sorted(hubs.items(), key=lambda x: x[1], reverse=True)
    for node, score in sorted_hubs[:20]:  # Top 10 nodes
        print(f"Node: {node}, Score: {score}")

    print("Authority-Werte:")
    sorted_authorities = sorted(authorities.items(), key=lambda x: x[1], reverse=True)
    for node, score in sorted_authorities[:20]:  # Top 10 nodes
        print(f"Node: {node}, Score: {score}")


def test_pagerank():
    # Test with a sample RDF file
    ttl_file = "data/flexidug.ttl"

    g = Graph()
    g.parse(ttl_file, format="turtle")

    graph = rdf2networkx(g)

    # HITS-Algorithmus ausführen
    pr = nx.pagerank(graph)

    print("Pagerank")
    sorted_pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)
    for node, score in sorted_pr[:20]:  # Top 10 nodes
        print(f"Node: {node}, Score: {score}")


def test_connected_components():
    # Test with a sample RDF file
    ttl_file = "data/flexidug.ttl"

    g = Graph()
    g.parse(ttl_file, format="turtle")

    graph = rdf2networkx(g,directed=False)
   

    # Alle verbundenen Komponenten finden (als Mengen von Knoten)
    components = list(nx.connected_components(graph))

    # Optional: Die Teilgraphen extrahieren
    subgraphs = [graph.subgraph(c).copy() for c in components]

    for i, sg in enumerate(subgraphs):
        print(f"Teilgraph {i + 1}: Knoten = {len(sg.nodes)} Example: {list(sg.nodes)[0]}")


def test_communities():
    # Test with a sample RDF file
    ttl_file = "data/flexidug.ttl"

    g = Graph()
    g.parse(ttl_file, format="turtle")

    graph = rdf2networkx(g)

    communities = greedy_modularity_communities(graph)

    for i, comm in enumerate(communities):
        print(f"Community {i + 1}: len={len(comm)} {sorted(comm)[0]}")

    # Subgraph erzeugen – enthält nur Knoten in 'knotenmenge' + ihre Kanten untereinander
    G_sub = graph.subgraph(communities[5]).copy()

    print("Knoten im Subgraphen:", len(G_sub.nodes()))
    print("Kanten im Subgraphen:", len(G_sub.edges()))
