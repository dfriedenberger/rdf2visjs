from rdf2vis.svg_utils import replace_placeholder

svg1 = replace_placeholder('transformation.svg', {"X": '1'})
svg2 = replace_placeholder('process.svg', {"PLATZHALTER": 'Process'})


# Ergebnis speichern
with open('transformation_generated.svg', 'w', encoding='utf-8') as f:
    f.write(svg1)
with open('process_generated.svg', 'w', encoding='utf-8') as f:
    f.write(svg2)
