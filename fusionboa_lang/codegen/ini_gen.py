"""
FusionBoa → INI Code Generator
Converts FusionBoa-style INI to real INI format.
"""

from typing import List


class IniGenerator:
    def __init__(self):
        self.output = []
        self.current_section = None

    def generate(self, source: str) -> str:
        self.output = []
        self.current_section = None
        lines = source.strip().split('\n')
        
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            
            if stripped.startswith('[') and stripped.endswith(']'):
                self.current_section = stripped
                self.output.append(stripped)
            elif ' ' in stripped or '\t' in stripped:
                parts = stripped.split(None, 1)
                if len(parts) == 2:
                    key = parts[0].strip('"').strip("'")
                    val = parts[1].strip('"').strip("'")
                    self.output.append(f'{key} = {val}')
                else:
                    self.output.append(stripped)
            else:
                self.output.append(stripped)
        
        return '\n'.join(self.output)


def generate_ini(source: str) -> str:
    gen = IniGenerator()
    return gen.generate(source)
