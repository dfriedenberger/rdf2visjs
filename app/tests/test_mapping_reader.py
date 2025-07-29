import pytest
from rdf2vis.mapping_reader import MappingReader
from pathlib import Path


@pytest.fixture
def mapping_yaml_file():
    """get path to YAML Test file."""
    path = Path(__file__).parent
    return path / "data/mapping.yaml"


def test_get_icon_for_uri(mapping_yaml_file):
    """Test URI expansion with namespaces."""
    mapping_reader = MappingReader(mapping_yaml_file)

    icon = mapping_reader.get_icon_for_uri("http://frittenburger.de/ontology/mmut#RDFMicroModel", None)
    assert icon == "/icons/rdf-model.svg"


def test_get_views(mapping_yaml_file):
    """Test getting views configuration."""
    mapping_reader = MappingReader(mapping_yaml_file)
    views = mapping_reader.get_views()

    assert ['mmut'] == list(views)


def test_contains_in_view(mapping_yaml_file):
    """Test checking if a URI is contained in a specific view."""
    mapping_reader = MappingReader(mapping_yaml_file)

    assert mapping_reader.contains_in_view('mmut', 'http://frittenburger.de/ontology/mmut#BinaryMicroModel')
    assert not mapping_reader.contains_in_view('mmut', 'http://example.org/xxx#NonExistentModel')

    with pytest.raises(ValueError):
        mapping_reader.contains_in_view('mmut', 'non_existent_uri')

    with pytest.raises(ValueError):
        mapping_reader.contains_in_view('non_existent_view', 'http://frittenburger.de/ontology/mmut#RDFMicroModel')
