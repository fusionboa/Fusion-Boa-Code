"""
FusionBoa Standard Library: System Operations

Natural English syntax for system interactions:
  wait 5 seconds
  get current time
  get environment variable "PATH"
"""

import time
import os
from datetime import datetime


class SystemClock:
    """System time and clock operations for FusionBoa programs."""

    @staticmethod
    def wait(seconds: float) -> None:
        """Pause execution for a number of seconds.
        
        FusionBoa syntax: wait 5 seconds
        """
        time.sleep(seconds)

    @staticmethod
    def wait_milliseconds(ms: int) -> None:
        """Pause execution for milliseconds.
        
        FusionBoa syntax: wait 500 milliseconds
        """
        time.sleep(ms / 1000.0)

    @staticmethod
    def current_time() -> str:
        """Get the current time as an ISO 8601 string.
        
        FusionBoa syntax: get current time
        """
        return datetime.now().isoformat()

    @staticmethod
    def current_timestamp() -> float:
        """Get the current Unix timestamp (seconds since epoch).
        
        FusionBoa syntax: get timestamp
        """
        return time.time()

    @staticmethod
    def current_date() -> str:
        """Get the current date as YYYY-MM-DD.
        
        FusionBoa syntax: get current date
        """
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def formatted_time(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Get the current time formatted.
        
        FusionBoa syntax: get time formatted as "YYYY-MM-DD HH:MM:SS"
        """
        return datetime.now().strftime(fmt)

    @staticmethod
    def elapsed(start_time: float) -> float:
        """Get elapsed seconds since a start time.
        
        FusionBoa syntax: time elapsed since start
        """
        return time.time() - start_time

    @staticmethod
    def get_env(name: str) -> str:
        """Get an environment variable.
        
        FusionBoa syntax: get environment variable "PATH"
        """
        return os.environ.get(name, "")

    @staticmethod
    def set_env(name: str, value: str) -> None:
        """Set an environment variable.
        
        FusionBoa syntax: set environment variable "DEBUG" to "true"
        """
        os.environ[name] = value
