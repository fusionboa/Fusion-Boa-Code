"""
FusionBoa → CSS Code Generator

Converts FusionBoa-style CSS rules into real CSS.

Fusion CSS syntax:
    style .container:
        display "flex"
        flex-direction "column"
        gap "20px"
        background-color "#f0f0f0"

    style #header:
        font-size "24px"
        font-weight "bold"

    style div.main:
        padding "10px"
        margin "0 auto"
"""

import re
from typing import List, Dict


class CssGenerator:
    """Generates CSS from FusionBoa-style rules."""

    def __init__(self):
        self.output = []
        self.indent_level = 0

    def _indent(self) -> str:
        return "  " * self.indent_level

    def generate(self, source: str) -> str:
        """Parse FusionBoa-style CSS source and generate CSS."""
        self.output = []
        self.indent_level = 0
        lines = source.strip().split('\n')
        self._parse_block(lines, 0)
        return '\n'.join(self.output)

    def _parse_block(self, lines: List[str], start_index: int) -> int:
        """Parse CSS rules from lines starting at start_index."""
        i = start_index
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            if not stripped or stripped.startswith('//'):
                i += 1
                continue
            # Only skip # comments (with space after #), not #id-selectors
            if stripped.startswith('# ') or stripped == '#':
                i += 1
                continue

            indent = len(line) - len(line.lstrip())
            if indent < self.indent_level * 2:
                break

            # Check for CSS rule or nested style
            # Rules start with 'style ', '@', or end with ':' (e.g. body:, .class:, *:)
            if stripped.startswith('style ') or stripped.startswith('@') or stripped.endswith(':'):
                consumed = self._parse_rule(lines, i)
                if consumed == i:
                    i += 1
                else:
                    i = consumed
            else:
                i += 1

        return i

    def _parse_rule(self, lines: List[str], start: int) -> int:
        """Parse a CSS rule with selector and properties."""
        line = lines[start]
        stripped = line.strip()

        # Parse selector (strip 'style ' prefix and trailing colon)
        if stripped.startswith('style '):
            selector = stripped[6:].strip().rstrip(':').strip()
        else:
            selector = stripped.rstrip(':').strip()

        # Check if there are inline properties or a block
        has_block = False
        if start + 1 < len(lines):
            next_line = lines[start + 1]
            next_indent = len(next_line) - len(next_line.lstrip())
            current_indent = len(lines[start]) - len(lines[start].lstrip())
            if next_indent > current_indent and next_line.strip():
                has_block = True

        if not has_block:
            # Single-line rule (would need inline props, but CSS has them on next lines)
            # Just output selector for now, properties will be on next lines
            self.output.append(f'{selector} {{')
            self.indent_level += 1
            next_idx = self._parse_properties(lines, start + 1)
            self.indent_level -= 1
            self.output.append('}')
            return next_idx
        else:
            self.output.append(f'{selector} {{')
            self.indent_level += 1
            next_idx = self._parse_properties(lines, start + 1)
            self.indent_level -= 1
            self.output.append('}')
            return next_idx

    def _unquote(self, val: str) -> str:
        """Strip only matching outer quotes from a value."""
        if len(val) >= 2:
            if (val[0] == '"' and val[-1] == '"') or (val[0] == "'" and val[-1] == "'"):
                return val[1:-1]
        return val

    def _parse_properties(self, lines: List[str], start: int) -> int:
        """Parse CSS properties within a block."""
        i = start
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            if not stripped or stripped.startswith('//'):
                i += 1
                continue
            # Only skip # comments (with space after #), not #id-selectors
            if stripped.startswith('# ') or stripped == '#':
                i += 1
                continue

            indent = len(line) - len(line.lstrip())
            if indent < self.indent_level * 2:
                break

            # Check for nested @media or style
            if stripped.startswith('style ') or stripped.startswith('@'):
                consumed = self._parse_rule(lines, i)
                if consumed > i:
                    i = consumed
                    continue

            # Parse property: name "value" or name value
            if ' ' in stripped or '\t' in stripped:
                parts = stripped.split(None, 1)
                if len(parts) == 2:
                    prop_name = parts[0]
                    prop_value = self._unquote(parts[1])
                    self.output.append(f'{self._indent()}{self._css_prop(prop_name)}: {prop_value};')
                else:
                    self.output.append(f'{self._indent()}{stripped}')
            else:
                self.output.append(f'{self._indent()}{stripped}')

            i += 1

        return i

    def _css_prop(self, name: str) -> str:
        """Convert a FusionBoa-style CSS property name to CSS format."""
        # Handle hyphenated names: backgroundColor -> background-color
        # and FusionBoa-style names
        replacements = {
            "background-color": "background-color",
            "background": "background",
            "color": "color",
            "font-size": "font-size",
            "font-family": "font-family",
            "font-weight": "font-weight",
            "margin": "margin",
            "padding": "padding",
            "border": "border",
            "border-radius": "border-radius",
            "display": "display",
            "position": "position",
            "width": "width",
            "height": "height",
            "max-width": "max-width",
            "min-width": "min-width",
            "max-height": "max-height",
            "min-height": "min-height",
            "top": "top",
            "bottom": "bottom",
            "left": "left",
            "right": "right",
            "gap": "gap",
            "flex-direction": "flex-direction",
            "flex": "flex",
            "flex-wrap": "flex-wrap",
            "justify-content": "justify-content",
            "align-items": "align-items",
            "align-content": "align-content",
            "text-align": "text-align",
            "text-decoration": "text-decoration",
            "overflow": "overflow",
            "z-index": "z-index",
            "opacity": "opacity",
            "transform": "transform",
            "transition": "transition",
            "animation": "animation",
            "cursor": "cursor",
            "list-style": "list-style",
            "box-shadow": "box-shadow",
            "grid-template": "grid-template",
            "grid-gap": "grid-gap",
        }
        
        # Convert camelCase to kebab-case for unknown properties
        result = name
        if result not in replacements:
            # Convert FusionBoa-style to kebab-case
            result = re.sub(r'([a-z])([A-Z])', r'\1-\2', name).lower()
            result = result.replace('_', '-')
        
        return result


def generate_css(source: str) -> str:
    """Generate CSS from FusionBoa-style source."""
    gen = CssGenerator()
    return gen.generate(source)
