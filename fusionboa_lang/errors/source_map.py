"""
FusionBoa Error Source-Map Vector

Maps generated target code line numbers back to original .fusboa source lines.
When a target language (Python, JS, etc.) throws an error at line 118 of the
generated code, this module intercepts and maps it back:

    [FusionBoa Error] Typo detected on Line 42 of your .fusboa file.
    Original: let x be something

Usage:
    from fusionboa_lang.errors.source_map import SourceMapper
    mapper = SourceMapper()
    mapper.record(original_line, generated_line_start, generated_line_end)
    original_line = mapper.map_back(generated_line_number)
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class SourceMapping:
    """Maps a range of generated lines back to an original source line."""
    original_line: int
    original_content: str = ""
    generated_start_line: int = 0
    generated_end_line: int = 0


@dataclass
class FusionBoaError:
    """A user-friendly error message mapped back to original source."""
    original_line: int
    original_col: int
    message: str
    source_snippet: str = ""
    severity: str = "error"


class SourceMapper:
    """Tracks line mappings between .fusboa source and generated target code.

    Each time the code generator outputs a line, the mapper records which
    original source line it corresponds to. When an error occurs in the
    generated code, map_back() finds the original line.
    """

    def __init__(self):
        self._mappings: List[SourceMapping] = []
        self._current_generated_line = 1
        self._original_source_lines: List[str] = []

    def set_original_source(self, source: str) -> None:
        """Store the original .fusboa source for error context."""
        self._original_source_lines = source.split('\n')

    def record(self, original_line: int, generated_line_count: int = 1,
               original_content: str = "") -> None:
        """Record a mapping from generated code back to original source.

        Args:
            original_line: The 1-based line number in .fusboa source
            generated_line_count: How many generated lines this maps to
            original_content: The original source line content
        """
        start = self._current_generated_line
        end = start + generated_line_count - 1
        self._mappings.append(SourceMapping(
            original_line=original_line,
            original_content=original_content,
            generated_start_line=start,
            generated_end_line=end,
        ))
        self._current_generated_line += generated_line_count

    def record_block(self, original_line: int, generated_line_count: int,
                     original_content: str = "") -> None:
        """Record a block mapping (e.g., for multi-line generated constructs)."""
        self.record(original_line, generated_line_count, original_content)

    def map_back(self, generated_line: int) -> Optional[SourceMapping]:
        """Map a generated code line back to original .fusboa line.

        Returns None if no mapping exists (e.g., generated boilerplate).
        """
        for mapping in self._mappings:
            if mapping.generated_start_line <= generated_line <= mapping.generated_end_line:
                return mapping
        return None

    def format_error(self, generated_line: int, generated_message: str,
                     generated_col: int = 0) -> FusionBoaError:
        """Format a generated error into a user-friendly FusionBoa error.

        Args:
            generated_line: Line number in generated code where error occurred
            generated_message: The error message from the target runtime
            generated_col: Column in generated code (from stack trace)

        Returns:
            FusionBoaError with original source line info
        """
        mapping = self.map_back(generated_line)

        if mapping:
            snippet = mapping.original_content
            if not snippet and 0 < mapping.original_line <= len(self._original_source_lines):
                snippet = self._original_source_lines[mapping.original_line - 1]

            return FusionBoaError(
                original_line=mapping.original_line,
                original_col=generated_col,
                message=generated_message,
                source_snippet=snippet,
                severity="error",
            )
        else:
            # Couldn't map - show the generated error as-is
            return FusionBoaError(
                original_line=generated_line,
                original_col=0,
                message=f"[Generated code] {generated_message}",
                source_snippet="(no source mapping available)",
                severity="warning",
            )

    def intercept_and_format(self, generated_line: int, error_msg: str,
                             generated_col: int = 0) -> str:
        """Intercept a generated error and produce a FusionBoa-formatted message.

        Returns a formatted string like:
            [FusionBoa Error] Typo detected on Line 42 of your .fusboa file
            Original: let x be something
        
        Args:
            generated_line: The line number in generated code
            error_msg: The error message
            generated_col: Column from stack trace

        Returns:
            User-friendly formatted error string
        """
        fb_error = self.format_error(generated_line, error_msg, generated_col)

        if fb_error.severity == "error":
            prefix = "[FusionBoa Error]"
        else:
            prefix = "[FusionBoa Warning]"

        lines = [
            f"{prefix} {fb_error.message}",
        ]

        if fb_error.source_snippet and fb_error.source_snippet != "(no source mapping available)":
            lines.append(f"    → Original line {fb_error.original_line}: {fb_error.source_snippet}")
        elif fb_error.severity == "warning":
            lines.append(f"    → Generated line {fb_error.original_line} (no .fusboa mapping)")

        return "\n".join(lines)


# ---- Executor Integration ----

class SourceMappedExecutor:
    """Wraps the FusionBoa executor with error source mapping capability.

    When the executor encounters an error, it uses the SourceMapper to
    produce user-friendly error messages pointing to the original .fusboa source.

    Usage:
        mapper = SourceMapper()
        mapper.set_original_source(fusboa_source_code)
        
        executor = SourceMappedExecutor(mapper)
        try:
            executor.execute(generated_code, target_language="python")
        except Exception as e:
            original_error = mapper.intercept_and_format(e.lineno, str(e))
            print(original_error)
    """

    def __init__(self, mapper: SourceMapper):
        self.mapper = mapper

    def execute(self, generated_code: str, target_language: str = "python") -> None:
        """Execute generated code with error source mapping.

        This is a placeholder that would integrate with the actual executor.
        In production, this would run the code and catch exceptions,
        mapping them back to original source lines.
        """
        try:
            if target_language == "python":
                exec(generated_code)
            elif target_language == "javascript":
                # Would use node.js subprocess
                pass
            else:
                raise NotImplementedError(f"Execution for {target_language} not implemented")
        except Exception as e:
            # Extract line number from error
            import traceback
            tb = traceback.extract_tb(e.__traceback__)
            if tb:
                frame = tb[-1]
                line = frame.lineno
                formatted = self.mapper.intercept_and_format(line, str(e))
                raise RuntimeError(formatted) from e
            raise

    def record_generation(self, original_line: int, generated_lines: str,
                          original_content: str = "") -> None:
        """Record a mapping during code generation.

        Called by the code generator for each original source statement.

        Args:
            original_line: Original .fusboa line number
            generated_lines: The generated code string
            original_content: Original .fusboa source line
        """
        line_count = generated_lines.count('\n') + 1
        self.mapper.record(
            original_line=original_line,
            generated_line_count=line_count,
            original_content=original_content,
        )


def create_source_mapper(source: str = "") -> SourceMapper:
    """Create a SourceMapper with the original source pre-loaded."""
    mapper = SourceMapper()
    if source:
        mapper.set_original_source(source)
    return mapper
