"""
FusionBoa -> Markdown Code Generator

Passes Markdown content through as-is.
Markdown uses # for headings, so we don't strip anything.
The @target pre-processor already removes annotation lines.
"""


def generate_markdown(source: str) -> str:
    """Generate Markdown from FusionBoa-style source.
    
    Simply returns the source as-is. Markdown syntax is already valid,
    and # characters are meaningful (headings, not FusionBoa comments).
    """
    return source.strip()
