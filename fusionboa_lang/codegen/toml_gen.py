"""
FusionBoa -> TOML Code Generator
Converts Fusion data structures to TOML format.
"""

from .helpers import parse_fusionboa_value


def _to_toml(obj, key_prefix="") -> str:
    """Convert Python object to TOML string."""
    lines = []
    
    if obj is None:
        return ""
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        escaped = obj.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        return f'"{escaped}"'
    if isinstance(obj, list):
        if not obj:
            return "[]"
        if all(not isinstance(item, (dict, list)) for item in obj):
            items = ", ".join(_to_toml(item) for item in obj)
            return f"[{items}]"
        return ""
    if isinstance(obj, dict):
        if not obj:
            return ""
        if key_prefix:
            lines.append(f"[{key_prefix}]")
        for k, v in obj.items():
            full_key = f"{key_prefix}.{k}" if key_prefix else k
            if isinstance(v, dict):
                sub = _to_toml(v, full_key)
                if sub:
                    lines.append(sub)
            elif isinstance(v, list) and v and all(isinstance(i, dict) for i in v):
                for item in v:
                    lines.append(f"[[{full_key}]]")
                    sub = _to_toml(item, "")
                    if sub:
                        lines.append(sub)
            else:
                lines.append(f"{k} = {_to_toml(v)}")
        return '\n'.join(lines)
    return str(obj)


def generate_toml(source: str) -> str:
    """Generate TOML from FusionBoa-style source."""
    try:
        data = parse_fusionboa_value(source)
        if data is None:
            return ""
        return _to_toml(data)
    except Exception as e:
        return source
