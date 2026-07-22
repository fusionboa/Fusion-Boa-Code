"""
FusionBoa Standard Library: File I/O

Natural English syntax for file operations:
  read file "data.txt"
  write "hello" to file "log.txt"
  append "line" to file "log.txt"
"""

import os
from pathlib import Path


class FileIO:
    """File input/output operations for FusionBoa programs."""

    @staticmethod
    def read_file(path: str) -> str:
        """Read entire file content.
        
        FusionBoa syntax: read file "data.txt"
        """
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def read_file_lines(path: str) -> list:
        """Read file lines as a list.
        
        FusionBoa syntax: read lines from file "data.txt"
        """
        with open(path, 'r', encoding='utf-8') as f:
            return [line.rstrip('\n') for line in f]

    @staticmethod
    def write_file(path: str, content: str) -> None:
        """Write content to a file (overwrites existing).
        
        FusionBoa syntax: write "hello" to file "log.txt"
        """
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(str(content))

    @staticmethod
    def append_file(path: str, content: str) -> None:
        """Append content to a file.
        
        FusionBoa syntax: append "line" to file "log.txt"
        """
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, 'a', encoding='utf-8') as f:
            f.write(str(content))

    @staticmethod
    def file_exists(path: str) -> bool:
        """Check if a file exists.
        
        FusionBoa syntax: file "data.txt" exists
        """
        return os.path.isfile(path)

    @staticmethod
    def delete_file(path: str) -> None:
        """Delete a file.
        
        FusionBoa syntax: delete file "old.txt"
        """
        if os.path.isfile(path):
            os.remove(path)

    @staticmethod
    def file_size(path: str) -> int:
        """Get file size in bytes.
        
        FusionBoa syntax: size of file "data.txt"
        """
        return os.path.getsize(path)
