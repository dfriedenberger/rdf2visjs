import re
from rdflib import Graph
from .sparql_wrapper import SparQLWrapper


def gen_graph():

    # RDF-Graph erzeugen
    g = Graph()

    # Datei im Turtle-Format einlesen

    # g.parse("data/friends.ttl", format="turtle")
    g.parse("data/flexidug.ttl", format="turtle")

    # Anzahl der Tripel anzeigen
    print(f"Graph hat {len(g)} Tripel.\n")

    nodes = []
    nodes_id = dict()
    node_id = 0

    # SVG Icons (können URLs zu externen SVG-Dateien sein)
    person_icon = "icons/person-svgrepo-com.svg"
    book_icon = "icons/book-svgrepo-com.svg"
    server_icon = "icons/server-svgrepo-com.svg"
    city_icon = "icons/city-svgrepo-com.svg"
    node_icon = "icons/node-svgrepo-com.svg"

    instance_types = set()
    sparql_wrapper = SparQLWrapper(g)
    for inst in sparql_wrapper.get_instances():

        icon = node_icon
        # Instanztyp abfragen
        inst_type = sparql_wrapper.get_type(inst)
        instance_types.add(inst_type)
        print(inst, "type:", inst_type)
        if inst_type.endswith("Person"):
            icon = person_icon
        elif inst_type.endswith("Place"):
            icon = city_icon

        label = str(inst)
        for prop, obj in sparql_wrapper.get_object_properties(inst):
            print(inst, "property:", prop, "object:", obj)
            if prop.endswith("name") or prop.endswith("label"):
                label = str(obj)

        node_id += 1
        nodes_id[inst] = node_id
        nodes.append({"id": node_id, "label": label, "shape": "image", "image": icon})

    edges = []
    for from_ref, ref, to_ref in sparql_wrapper.get_references():
        print(from_ref, ref, to_ref)

        label = re.split(r'[/#](?=[^/#]*$)', str(ref))[-1]

        edges.append({"from": nodes_id[from_ref], "to": nodes_id[to_ref], "label": label})

    # Tripel ausgeben (Subjekt - Prädikat - Objekt)
    #for subj, pred, obj in g:
    #    print(f"{subj} -- {pred} --> {obj}")

    it = sorted(list(instance_types))
    print("Instance types:", it)

    return {
        "nodes": nodes,
        "edges": edges
    }
