"""
Fusion Target Router

Splits a .fusboa file into sections by // @target, // @raw, // @native annotations.
Each section is routed to the appropriate codegen.
Supports: python, js, ts, ruby, go, rust, cpp, julia, r, kotlin,
         swift, java, csharp, lua, html, css, json, yaml, toml,
         xml, markdown, ini, react

Native passthrough: // @raw python, // @native js, // @passthrough css
This lets users write native code for any target language.
"""

import re
from typing import Dict, List, Optional
from pathlib import Path


# File extensions per target
TARGET_EXTENSIONS = {
    # Programming languages
    "python": ".py", "py": ".py",
    "javascript": ".js", "js": ".js",
    "typescript": ".ts", "ts": ".ts",
    "ruby": ".rb", "rb": ".rb",
    "go": ".go", "golang": ".go",
    "rust": ".rs", "rs": ".rs",
    "cpp": ".cpp", "c++": ".cpp",
    "julia": ".jl", "jl": ".jl",
    "r": ".r",
    "kotlin": ".kt", "kt": ".kt",
    "swift": ".swift",
    "java": ".java",
    "csharp": ".cs", "cs": ".cs", "c#": ".cs",
    "lua": ".lua",
    # Markup & data formats
    "html": ".html", "htm": ".html",
    "css": ".css",
    "json": ".json",
    "yaml": ".yaml", "yml": ".yaml",
    "toml": ".toml",
    "xml": ".xml",
    "markdown": ".md", "md": ".md",
    "ini": ".ini", "cfg": ".ini",
    "react": ".jsx", "jsx": ".jsx",
}


def split_by_target(source: str) -> Dict[str, List[str]]:
    """
    Split Fusion source by // @target, // @raw, // @native, // @passthrough annotations.
    
    Returns a dict mapping target names to lists of source lines.
    Lines before the first annotation go to "fusion" (default).
    
    Native passthrough sections are marked with a "__raw__" prefix in the key
    so the caller knows to pass them through without FusionBoa compilation.
    """
    sections: Dict[str, List[str]] = {}
    current_target = "fusion"
    sections[current_target] = []
    
    # Match: // @target python, // @raw js, // @native go, // @passthrough css
    target_pattern = re.compile(r'^\s*(//|#)\s*@(target|raw|native|passthrough)\s+(\S+)')
    
    for line in source.split('\n'):
        match = target_pattern.match(line)
        if match:
            annotation_type = match.group(2).strip().lower()  # target, raw, native, or passthrough
            target_name = match.group(3).strip().lower()
            is_raw = annotation_type in ("raw", "native", "passthrough")
            
            if is_raw:
                # Native/raw sections use __raw__ prefix in key for identification
                current_target = f"__raw__{target_name}"
            else:
                current_target = target_name
            
            if current_target not in sections:
                sections[current_target] = []
            # Don't include the annotation line itself
            continue
        sections[current_target].append(line)
    
    # Clean up each section
    result = {}
    for target, lines in sections.items():
        # Remove leading/trailing blank lines
        while lines and lines[-1].strip() == '':
            lines.pop()
        while lines and lines[0].strip() == '':
            lines.pop(0)
        # Remove leading/trailing comment-only lines (separator banners)
        def _is_separator(line):
            """Check if a line is a comment-only separator (e.g. # =====, # ----)"""
            s = line.strip()
            if not s.startswith('#'):
                return False
            content = s.lstrip('#').strip()
            if not content:
                return True
            if all(not c.isalnum() for c in content):
                return True
            return False
        
        while lines and _is_separator(lines[0]):
            lines.pop(0)
        while lines and _is_separator(lines[-1]):
            lines.pop()
        # Only strip trailing comments for non-raw sections
        # Raw/native sections preserve all comments as they're user's native code
        if not target.startswith("__raw__"):
            def _is_comment(line):
                s = line.strip()
                return s.startswith('#') or s.startswith('//')
            while lines and _is_comment(lines[-1]):
                lines.pop()
        result[target] = lines
    
    return result


def is_raw_section(target_key: str) -> bool:
    """Check if a section key is a native/raw passthrough."""
    return target_key.startswith("__raw__")


def get_raw_target(target_key: str) -> str:
    """Extract the actual target name from a raw section key."""
    if target_key.startswith("__raw__"):
        return target_key[7:]  # Strip "__raw__" prefix
    return target_key


def get_extension(target: str) -> str:
    """Get the file extension for a target language/format."""
    return TARGET_EXTENSIONS.get(target, f".{target}")


def is_programming_language(target: str) -> bool:
    """Check if a target is a programming language (vs markup/data format)."""
    prog_langs = {
        "python", "py", "javascript", "js", "typescript", "ts",
        "ruby", "rb", "go", "golang", "rust", "rs",
        "cpp", "c++", "julia", "jl", "r",
        "kotlin", "kt", "swift", "java",
        "csharp", "cs", "c#", "lua",
        "react", "jsx",
    }
    return target in prog_langs


def build_output_filename(base_name: str, target: str) -> str:
    """Build the output filename for a target."""
    ext = get_extension(target)
    return f"{base_name}{ext}"


def build_all_filenames(base_name: str, targets: List[str]) -> Dict[str, str]:
    """Build output filenames for all targets."""
    return {t: build_output_filename(base_name, t) for t in targets}
