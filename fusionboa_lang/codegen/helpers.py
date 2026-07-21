"""
Shared helper utilities for code generators.
"""

from .data_parser import parse_data


def parse_fusionboa_value(source: str):
    """Parse a FusionBoa-style data value from source.
    
    Uses the dedicated data parser which handles multi-line dicts,
    Fusion keywords as keys, comments, and nested structures.
    
    Returns a Python object (dict, list, str, int, float, bool, None).
    """
    try:
        return parse_data(source)
    except Exception as e:
        return None
