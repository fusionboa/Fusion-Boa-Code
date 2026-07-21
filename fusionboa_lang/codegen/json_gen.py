"""
FusionBoa -> JSON Code Generator
Converts Fusion data structures to JSON.
"""

from .helpers import parse_fusionboa_value


def _to_json(obj, indent: int = 0) -> str:
    """Convert Python object to JSON string."""
    prefix = "  " * indent
    
    if obj is None:
        return "null"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        escaped = (obj.replace('\\', '\\\\')
                     .replace('"', '\\"')
                     .replace('\n', '\\n')
                     .replace('\r', '\\r')
                     .replace('\t', '\\t'))
        return f'"{escaped}"'
    if isinstance(obj, list):
        if not obj:
            return "[]"
        items = []
        for item in obj:
            items.append(f"{prefix}  {_to_json(item, indent + 1)}")
        return "[\n" + ",\n".join(items) + f"\n{prefix}]"
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        items = []
        for k, v in obj.items():
            key = _to_json(k, indent + 1)
            val = _to_json(v, indent + 1)
            items.append(f"{prefix}  {key}: {val}")
        return "{\n" + ",\n".join(items) + f"\n{prefix}}}"
    return str(obj)


def generate_json(source: str) -> str:
    """Generate JSON from FusionBoa-style source."""
    try:
        data = parse_fusionboa_value(source)
        if data is None:
            return "{}"
        return _to_json(data)
    except Exception as e:
        return source
