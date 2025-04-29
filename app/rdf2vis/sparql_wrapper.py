import string
import re
from rdflib import Literal


class SparQLWrapper:

    def __init__(self, graph):
        self.graph = graph

    def get_references(self):
        q = """
            SELECT ?s ?p ?o
            WHERE {
                ?s ?p ?o .
                ?s a ?t1 .
                ?o a ?t2 .
            }
            """

        return [(r['s'], r['p'], r['o']) for r in self.graph.query(q)]

    def get_type(self, obj):
        q = """
            SELECT ?t
            WHERE {
                ?s a ?t .
            }
            """
        n = [r['t'] for r in self.graph.query(q, initBindings={'s': obj})]
        if len(n) != 1:
            raise ValueError(f"Not a single result: {n} for {obj}")
        return n[0]

    def get_instances(self):
        q = """
            SELECT ?s
            WHERE {
                ?s a ?t .
            }
            """
        n = [r['s'] for r in self.graph.query(q)]
        return n

    def get_object_properties(self, obj):
        q = """
            SELECT ?p ?o
            WHERE {
                ?s ?p ?o .
                FILTER NOT EXISTS {
                    ?o a ?t2 .
                }
            }
            """

        return [(r['p'], r['o']) for r in self.graph.query(q, initBindings={'s': obj})]

    def get_single_object_property(self, obj, prop):

        q = string.Template("""
            SELECT ?value
            WHERE {
                ?s <$PROP> ?value .
            }
            """).substitute(PROP=prop)

        n = [r['value'] for r in self.graph.query(q, initBindings={'s': obj})]
        if len(n) != 1:
            raise ValueError(f"Not a single result {str(n)} for {obj} prop: {prop}")
        if isinstance(n[0], Literal):
            return n[0].value
        return n[0]

    def get_in_references(self, obj, prop):
        q = string.Template("""
            SELECT ?s
            WHERE {
                ?s <$PROP> ?o .
                ?s a ?t .
            }
            """).substitute(PROP=prop)

        n = [r['s'] for r in self.graph.query(q, initBindings={'o': obj})]
        return n

    def get_out_references(self, obj, prop):
        q = string.Template("""
            SELECT ?o
            WHERE {
                ?s <$PROP> ?o .
                ?o a ?t .
            }
            """).substitute(PROP=prop)

        n = [r['o'] for r in self.graph.query(q, initBindings={'s': obj})]
        return n

    def get_out(self, obj):
        q = """
            SELECT ?p ?o
            WHERE {
                ?s ?p ?o .
            }
            """

        n = [(r['p'], r['o']) for r in self.graph.query(q, initBindings={'s': obj})]
        return n

    def get_single_out_reference(self, obj, prop):
        r = self.get_out_references(obj, prop)
        if len(r) != 1:
            raise ValueError(f"Not a single result {str(r)} for {obj}")
        return r[0]

    def has_out_reference(self, obj, prop):
        r = self.get_out_references(obj, prop)
        return len(r) > 0

    def get_sequence(self, obj):
        q = """
            SELECT ?position ?routeSection
            WHERE {
                # Finde die Elemente der rdf:Seq
                ?seq ?position ?routeSection .

                # Filtere nur Positionen wie rdf:_1, rdf:_2, usw.
                FILTER(STRSTARTS(STR(?position), STR(rdf:_)))
            }
            """
        n = []
        # Parse das Ergebnis
        for r in self.graph.query(q, initBindings={'seq': obj}):
            pos = int(re.search('#_(\\d+)$', r['position']).group(1))
            n.append((pos, r['routeSection']))

        # Sortiere die Liste nach dem ersten Element im Tupel (der Zahl)
        s = sorted(n, key=lambda x: x[0])

        # Extrahiere das zweite Element (den String) aus den sortierten Tupeln
        return [x[1] for x in s]
