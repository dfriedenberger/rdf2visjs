import yaml
from pathlib import Path
from typing import Dict, List
import fnmatch
import re


class MappingReader:
    """Reader for MMUT mapping YAML configuration files."""

    def __init__(self, yaml_file: str):
        self.yaml_file = Path(yaml_file)
        with open(self.yaml_file, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        self.namespaces = self.config.get('namespaces', {})

    def matches_uri(self, uri: str, pattern: str) -> bool:
        """Check if a URI matches a given pattern."""
        # Wenn pattern mit regex [a-z]: beginnt, dann namespace einsetzen

        if re.match(r'(^[a-z]+:)', pattern):
            namespace, _, local_part = pattern.partition(':')
            pattern = self.namespaces[namespace] + local_part

        # Handle full URIs or patterns
        return fnmatch.fnmatch(uri, pattern)

    def uri_in(self, uri: str, uris: List[str]) -> bool:
        """Check if a URI is in a list of URIs. List also can contain * or hello*"""
        for pattern in uris:
            if self.matches_uri(uri, pattern):
                return True
        return False

    def get_icon_for_uri(self, uri: str, default_uri: str) -> str:
        """Get icon path for a given URI (full or prefixed)."""

        # Try direct lookup first
        for pattern, icon in self.config.get('mappings', {}).items():
            if self.matches_uri(uri, pattern):
                return icon

        return default_uri

    def get_views(self) -> Dict:
        """Get all configured views."""
        return list(self.config.get("views", {}).keys())

    def get_view_config(self, view: str) -> Dict:
        """Get configuration for a specific view."""
        if view not in self.config.get("views", {}):
            raise ValueError(f"View '{view}' not found.")
        return self.config["views"][view]

    def contains_in_view(self, view: str, uri: str) -> bool:
        """Check if a URI is contained in a specific view."""
        v = self.get_view_config(view)
        includes = v.get('include', [])
        excludes = v.get('exclude', [])
        if self.uri_in(uri, includes):
            return True
        if self.uri_in(uri, excludes):
            return False
        raise ValueError(f"View '{view}' not found or does not contain URI '{uri}'.")
