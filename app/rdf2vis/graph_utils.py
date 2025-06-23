import re
from rdflib import Graph
from .sparql_wrapper import SparQLWrapper


def gen_graph(filename, mapping_file):

    # RDF-Graph erzeugen
    g = Graph()

    # Datei im Turtle-Format einlesen

    g.parse(filename, format="turtle")

    # Anzahl der Tripel anzeigen
    print(f"Graph hat {len(g)} Tripel.\n")

    nodes = []
    nodes_id = dict()
    node_id = 0

    icon_mapping = dict()
    with open(mapping_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue
            # Mapping-Definitionen einlesen
            p = line.split(r' ')
            if len(p) != 2:
                print(f"Fehlerhafte Mapping-Definition: {line} => {p}")
                continue
            # Mapping-Definitionen speichern
            icon_mapping[p[0]] = p[1]

    instance_types = set()
    sparql_wrapper = SparQLWrapper(g)
    for inst in sparql_wrapper.get_instances():

        icon = "/icons/node-svgrepo-com.svg"
        user_data = {
            "type": "None",
            "comment": "...",
        }
        # Instanztyp abfragen
        inst_type = str(sparql_wrapper.get_type(inst))
        instance_types.add(inst_type)
        print(inst, "type:", inst_type, icon_mapping)
        if inst_type in icon_mapping:
            icon = icon_mapping[inst_type]
        user_data["type"] = inst_type.split("#")[-1]  # Nur den letzten Teil des Typs verwenden

        label = str(inst)
        for prop, obj in sparql_wrapper.get_object_properties(inst):
            print(inst, "property:", prop, "object:", obj)
            if prop.endswith("name") or prop.endswith("label"):
                label = str(obj)
            if prop.endswith("comment"):
                user_data["comment"] = str(obj)

        if "{{label}}" in icon:
            # Platzhalter im Icon ersetzen und Label löschen
            print("Replacing label in icon:", icon)
            icon = icon.replace("{{label}}", label)
            label = ""

        node_id += 1
        nodes_id[inst] = node_id
        nodes.append({"id": node_id, "label": label, "shape": "image", "image": icon, "user_data": user_data})

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
