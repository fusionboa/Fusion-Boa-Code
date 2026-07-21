"""
FusionBoa -> HTML Code Generator

Converts FusionBoa-style HTML markup into real HTML.

Fusion HTML syntax:
    html lang "en":
        head:
            title "My Page"
        body class "container":
            h1 "Hello!"
            div id "content":
                p "Some text"
            img src "logo.png" alt "Logo"/
            input type "text" placeholder "Name"/
"""

from typing import List


class HtmlGenerator:
    """Generates HTML from FusionBoa-style markup."""

    VOID_ELEMENTS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }

    def __init__(self):
        self.output = []
        self.indent_stack = [-1]  # Stack of source indent levels (-1 ensures top-level elements work)

    def _indent(self) -> str:
        return "  " * (len(self.indent_stack) - 1)

    def generate(self, source: str) -> str:
        self.output = []
        self.indent_stack = [-1]
        lines = source.strip().split('\n')
        self._parse_block(lines, 0)
        return '\n'.join(self.output)

    def _get_indent(self, line: str) -> int:
        """Get the indentation level of a line (in spaces)."""
        return len(line) - len(line.lstrip())

    def _parse_block(self, lines: List[str], start_index: int) -> int:
        """Parse a block of HTML elements. Returns the next line index."""
        current_indent = self.indent_stack[-1]
        i = start_index
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            if not stripped or stripped.startswith('#'):
                i += 1
                continue

            indent = self._get_indent(line)
            
            # If indentation is at or before the parent level, we're done with this block
            if indent <= current_indent and i > start_index:
                break

            consumed = self._parse_element(lines, i)
            i = consumed if consumed > i else i + 1

        return i

    def _parse_element(self, lines: List[str], start: int) -> int:
        """Parse a single HTML element. Returns the next line index."""
        line = lines[start]
        stripped = line.strip()
        
        # Strip trailing colon (Fusion block syntax) and check for self-closing
        stripped = stripped.rstrip(':').strip()
        self_closing = stripped.endswith('/')
        if self_closing:
            stripped = stripped[:-1].strip()

        parts = self._tokenize_line(stripped)
        if not parts:
            return start + 1

        tag = parts[0].lower()
        
        # Handle doctype special tag: doctype html -> <!DOCTYPE html>
        if tag == "doctype":
            doc_type = "html"
            if len(parts) > 1:
                doc_type = parts[1].strip('"').strip("'")
            self.output.append(f'{self._indent()}<!DOCTYPE {doc_type.upper()}>')
            return start + 1
        
        source_indent = self._get_indent(line)

        # Parse attributes and text content
        attributes = {}
        text_content = None
        i = 1
        while i < len(parts):
            if parts[i] == ':':
                # Skip colon (Fusion block/content separator)
                i += 1
            elif i + 1 < len(parts) and (parts[i + 1].startswith('"') or parts[i + 1].startswith("'")):
                attr = parts[i].rstrip('=')  # strip trailing = from token like "class="
                val = parts[i + 1].strip('"').strip("'")
                attributes[attr] = val
                i += 2
            elif parts[i] == ',':
                i += 1
            elif parts[i].endswith('=') and i + 1 < len(parts):
                # Handle "class=" followed by "value" where the value was split by a space
                attr = parts[i].rstrip('=')
                val = parts[i + 1].strip('"').strip("'")
                attributes[attr] = val
                i += 2
            else:
                text_content = parts[i].strip('"').strip("'")
                i += 1

        attr_str = ''.join(f' {k}="{v}"' for k, v in attributes.items())
        is_void = tag in self.VOID_ELEMENTS or self_closing

        # Check if there's a child block
        has_children = False
        if start + 1 < len(lines):
            next_line = lines[start + 1]
            next_indent = self._get_indent(next_line)
            if next_indent > source_indent and next_line.strip() and not next_line.strip().startswith('#'):
                has_children = True

        # Generate HTML
        if is_void:
            self.output.append(f'{self._indent()}<{tag}{attr_str} />')
            return start + 1
        elif text_content and not has_children:
            self.output.append(f'{self._indent()}<{tag}{attr_str}>{self._escape(text_content)}</{tag}>')
            return start + 1
        elif not text_content and not has_children:
            self.output.append(f'{self._indent()}<{tag}{attr_str}></{tag}>')
            return start + 1
        else:
            # Element with children
            self.output.append(f'{self._indent()}<{tag}{attr_str}>')
            if text_content:
                self.output.append(f'{self._indent()}  {self._escape(text_content)}')
            if has_children:
                self.indent_stack.append(source_indent)
                next_idx = self._parse_block(lines, start + 1)
                self.indent_stack.pop()
                self.output.append(f'{self._indent()}</{tag}>')
                return next_idx
            self.output.append(f'{self._indent()}</{tag}>')
            return start + 1

    def _tokenize_line(self, line: str) -> List[str]:
        """Tokenize a line into parts, respecting quoted strings."""
        parts = []
        i = 0
        while i < len(line):
            if line[i] in ('"', "'"):
                quote = line[i]
                j = i + 1
                while j < len(line) and line[j] != quote:
                    if line[j] == '\\':
                        j += 1
                    j += 1
                parts.append(line[i:j+1])
                i = j + 1
            elif line[i] in (' ', '\t'):
                i += 1
            else:
                j = i
                while j < len(line) and line[j] not in (' ', '\t', '"', "'"):
                    j += 1
                parts.append(line[i:j])
                i = j
        return parts

    def _escape(self, text: str) -> str:
        return (text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;'))


def generate_html(source: str) -> str:
    gen = HtmlGenerator()
    return gen.generate(source)
