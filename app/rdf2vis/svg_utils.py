import re
import xml.etree.ElementTree as ET


def replace_placeholder(svg_file: str, replacements: dict) -> str:
    """
    Replace placeholder text in an SVG file with the given text.
    :param svg_file: Path to the SVG file.
    :param text: Text to replace the placeholder in the SVG file.
    :return: Processed SVG file as a string.
    """
    def replace_match(match):
        key = match.group(1)
        val = replacements.get(key, match.group(0))
        print(f"Replacing in {key} with {val}")
        return val

    # Load SVG file
    tree = ET.parse(f'static/icons/{svg_file}')
    root = tree.getroot()

    # Define SVG namespace
    ns = {'svg': 'http://www.w3.org/2000/svg'}

    # Search for all text elements and replace placeholders
    for tag in ['svg:tspan', 'svg:text']:
        for text_element in root.findall(f'.//{tag}', ns):
            if text_element.text:
                text_element.text = re.sub(r'\[([^\[\]]+)\]', replace_match, text_element.text)

    # Save result to a string
    return ET.tostring(root, encoding='unicode')
