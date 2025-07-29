import re
from rdflib import Graph
from .sparql_wrapper import SparQLWrapper
from .mapping_reader import MappingReader

def gen_graph(filename, mapping_yaml_file):

    # RDF-Graph erzeugen
    g = Graph()

    # Datei im Turtle-Format einlesen

    g.parse(filename, format="turtle")

    # Anzahl der Tripel anzeigen
    print(f"Graph hat {len(g)} Tripel.\n")

    nodes = []
    nodes_id = dict()
    node_id = 0

    # Mapping-Datei einlesen
    mapping_reader = MappingReader(mapping_yaml_file)
    views = mapping_reader.get_views()

    instance_types = set()
    sparql_wrapper = SparQLWrapper(g)
    for inst in sparql_wrapper.get_instances():

        user_data = {
            "type": "None",
            "label": "-"
        }
        attributes = {}
        # Instanztyp abfragen
        inst_type = str(sparql_wrapper.get_type(inst))
        instance_types.add(inst_type)

        icon = mapping_reader.get_icon_for_uri(inst_type, "/icons/node-svgrepo-com.svg")
        print(inst, "type:", inst_type, icon)

        user_data["type"] = inst_type.split("#")[-1]  # Nur den letzten Teil des Typs verwenden
        label = str(inst)
        for prop, obj in sparql_wrapper.get_object_properties(inst):
            print(inst, "property:", prop, "object:", obj)
            key = prop.split("#")[-1]  # Nur den letzten Teil des Properties verwenden
            if key == "name" or key == "label":
                label = str(obj)
            elif key == "comment":
                user_data["comment"] = str(obj)
            elif key == "type":
                # ignore type property
                continue
            else:
                attributes[key] = str(obj)

        if attributes:
            user_data["attributes"] = attributes
        user_data["label"] = label

        if "{{label}}" in icon:
            # Platzhalter im Icon ersetzen und Label löschen
            print("Replacing label in icon:", icon)
            icon = icon.replace("{{label}}", label)
            label = ""

        node_id += 1
        nodes_id[inst] = node_id

        # Views
        user_data["views"] = []
        for view in views:
            if mapping_reader.contains_in_view(view, inst_type):
                user_data["views"].append(view)

        nodes.append({"id": node_id, "label": label, "shape": "image", "image": icon, "user_data": user_data})

    edges = []
    for from_ref, ref, to_ref in sparql_wrapper.get_references():
        print(from_ref, ref, to_ref)

        label = re.split(r'[/#](?=[^/#]*$)', str(ref))[-1]

        edges.append({"from": nodes_id[from_ref], "to": nodes_id[to_ref], "label": label})

    it = sorted(list(instance_types))
    print("Instance types:", it)

    view_lables = {}
    for view in views:
        view_lables[view] = mapping_reader.get_view_config(view)["name"]

    return {
        "views": view_lables,
        "nodes": nodes,
        "edges": edges
    }
