"""
FusionBoa -> YAML Code Generator
Converts Fusion data structures to YAML format.
"""

from .helpers import parse_fusionboa_value


def _to_yaml(obj, indent=0) -> str:
    """Convert Python object to YAML string."""
    prefix = "  " * indent
    
    if obj is None:
        return "null"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        if any(c in obj for c in [':', '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`']):
            return f"'{obj}'"
        return obj
    if isinstance(obj, list):
        if not obj:
            return "[]"
        items = []
        for item in obj:
            items.append(f"{prefix}- {_to_yaml(item, indent + 1).lstrip()}")
        return '\n'.join(items)
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        items = []
        for k, v in obj.items():
            v_str = _to_yaml(v, indent + 1)
            if '\n' in v_str:
                items.append(f"{prefix}{k}:\n{v_str}")
            else:
                items.append(f"{prefix}{k}: {v_str}")
        return '\n'.join(items)
    return str(obj)


def generate_yaml(source: str) -> str:
    """Generate YAML from FusionBoa-style source."""
    try:
        data = parse_fusionboa_value(source)
        if data is None:
            return "{}"
        return _to_yaml(data)
    except Exception as e:
        return source
