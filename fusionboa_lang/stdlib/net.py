"""
FusionBoa Standard Library: Networking (HTTP)

Natural English syntax for web operations:
  fetch data from web url "https://api.com"
  post data to url "https://api.com" with body {"key": "value"}
"""

import urllib.request
import urllib.error
import json
from typing import Optional, Dict, Any


class Http:
    """HTTP networking operations for FusionBoa programs."""

    _TIMEOUT_SECONDS = 30

    @staticmethod
    def fetch(url: str, method: str = "GET", body: Optional[str] = None,
              headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Perform an HTTP request.
        
        FusionBoa syntax: fetch data from web url "https://api.com"

        Returns: dict with 'status', 'body', and 'headers' keys.
        """
        req = urllib.request.Request(url, method=method)
        
        default_headers = {"User-Agent": "FusionBoa/1.0", "Accept": "application/json"}
        all_headers = {**default_headers, **(headers or {})}
        for key, value in all_headers.items():
            req.add_header(key, value)
        
        data = body.encode('utf-8') if body else None

        try:
            with urllib.request.urlopen(req, data=data, timeout=Http._TIMEOUT_SECONDS) as response:
                return {
                    "status": response.status,
                    "body": response.read().decode('utf-8'),
                    "headers": dict(response.headers),
                }
        except urllib.error.HTTPError as e:
            return {
                "status": e.code,
                "body": e.read().decode('utf-8') if e.fp else str(e),
                "headers": dict(e.headers),
            }
        except Exception as e:
            return {
                "status": 0,
                "body": str(e),
                "headers": {},
            }

    @staticmethod
    def get(url: str) -> Dict[str, Any]:
        """HTTP GET request.
        
        FusionBoa syntax: get from url "https://api.com/items"
        """
        return Http.fetch(url, method="GET")

    @staticmethod
    def post(url: str, data: Any) -> Dict[str, Any]:
        """HTTP POST request.
        
        FusionBoa syntax: post data to url "https://api.com" with body data
        """
        body = json.dumps(data) if not isinstance(data, str) else data
        headers = {"Content-Type": "application/json"}
        return Http.fetch(url, method="POST", body=body, headers=headers)

    @staticmethod
    def put(url: str, data: Any) -> Dict[str, Any]:
        """HTTP PUT request."""
        body = json.dumps(data) if not isinstance(data, str) else data
        headers = {"Content-Type": "application/json"}
        return Http.fetch(url, method="PUT", body=body, headers=headers)

    @staticmethod
    def delete(url: str) -> Dict[str, Any]:
        """HTTP DELETE request.
        
        FusionBoa syntax: delete from url "https://api.com/item/1"
        """
        return Http.fetch(url, method="DELETE")
