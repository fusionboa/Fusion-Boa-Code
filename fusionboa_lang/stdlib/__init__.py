"""
FusionBoa Standard Library (stdlib)

Provides plain-English phrases for real-world interactions:
- File I/O: read/write files
- Networking: HTTP requests
- System: time, sleep, environment

These are integrated into the FusionBoa runtime via the executor
and exposed to .fusboa programs through natural syntax.
"""

from .io import FileIO
from .net import Http
from .system import SystemClock

__all__ = ["FileIO", "Http", "SystemClock"]
