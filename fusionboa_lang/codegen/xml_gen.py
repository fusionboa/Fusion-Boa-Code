"""
FusionBoa → XML Code Generator
Converts FusionBoa-style XML markup to real XML.
"""

from typing import List


class XmlGenerator:
    def __init__(self):
        self.output = []
        self.indent_level = 0

    def _indent(self) -> str:
        return "  " * self.indent_level

    def generate(self, source: str) -> str:
        self.output = ['<?xml version="1.0" encoding="UTF-8"?>']
        self.indent_level = 0
        lines = source.strip().split('\n')
        self._parse_block(lines, 0)
        return '\n'.join(self.output)

    def _parse_block(self, lines: List[str], start: int) -> int:
        i = start
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                i += 1
                continue
            indent = len(line) - len(line.lstrip())
            if indent < self.indent_level * 2:
                break
            consumed = self._parse_element(lines, i)
            i = consumed if consumed > i else i + 1
        return i

    def _parse_element(self, lines: List[str], start: int) -> int:
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

        tag = parts[0]
        attributes = {}
        text_content = None
        i = 1
        while i < len(parts):
            if i + 1 < len(parts) and (parts[i + 1].startswith('"') or parts[i + 1].startswith("'")):
                attr = parts[i]
                val = parts[i + 1].strip('"').strip("'")
                attributes[attr] = val
                i += 2
            else:
                text_content = parts[i].strip('"').strip("'")
                i += 1

        attr_str = ''.join(f' {k}="{v}"' for k, v in attributes.items())

        has_children = False
        if start + 1 < len(lines):
            next_line = lines[start + 1]
            next_indent = len(next_line) - len(next_line.lstrip())
            current_indent = len(lines[start]) - len(lines[start].lstrip())
            if next_indent > current_indent and next_line.strip() and not next_line.strip().startswith('#'):
                has_children = True

        if self_closing:
            self.output.append(f'{self._indent()}<{tag}{attr_str} />')
            return start + 1
        elif text_content and not has_children:
            self.output.append(f'{self._indent()}<{tag}{attr_str}>{self._escape(text_content)}</{tag}>')
            return start + 1
        else:
            self.output.append(f'{self._indent()}<{tag}{attr_str}>')
            if text_content:
                self.indent_level += 1
                self.output.append(f'{self._indent()}{self._escape(text_content)}')
                self.indent_level -= 1
            if has_children:
                self.indent_level += 1
                next_idx = self._parse_block(lines, start + 1)
                self.indent_level -= 1
                self.output.append(f'{self._indent()}</{tag}>')
                return next_idx
            self.output.append(f'{self._indent()}</{tag}>')
            return start + 1

    def _tokenize_line(self, line: str) -> List[str]:
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


def generate_xml(source: str) -> str:
    gen = XmlGenerator()
    return gen.generate(source)
