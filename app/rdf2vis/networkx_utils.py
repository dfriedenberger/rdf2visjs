import networkx as nx
from .sparql_wrapper import SparQLWrapper


def rdf2networkx(g, directed=True):
    """
    Convert an RDF graph to a NetworkX graph.

    Parameters
    ----------
    g : rdflib.Graph
        The RDF graph to convert.
    directed : bool, optional
        Whether to create a directed graph (default is False).

    Returns
    -------
    networkx.Graph or networkx.DiGraph
        The converted NetworkX graph.
    """

    if directed:
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()


    sparql_wrapper = SparQLWrapper(g)

    for from_ref, ref, to_ref in sparql_wrapper.get_references():
        graph.add_node(from_ref)
        graph.add_node(to_ref)
        graph.add_edge(from_ref, to_ref, predicate=ref)

    return graph
