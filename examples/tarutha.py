"""A tiny client for the Tarutha API, using only the Python standard library."""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("TARUTHA_API_BASE", "https://api.tarutha.co")
# Tarutha's edge refuses some default library user agents (Python's urllib among them),
# so every request names itself.
USER_AGENT = "tarutha-quickstart/1.0"


class TaruthaError(Exception):
    pass


def get(path, key_required=True, **params):
    """GET a Tarutha route and return the decoded JSON body.

    Pass query parameters as keywords. `from` is a Python keyword, so use
    get(path, **{"from": "2026-01"}).
    """
    key = os.environ.get("TARUTHA_API_KEY")
    if key_required and not key:
        sys.exit("Set TARUTHA_API_KEY first. Keys come with a Tarutha membership: "
                 "https://tarutha.co/#pricing")
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    url = BASE + path + ("?" + query if query else "")
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if key:
        headers["Authorization"] = "Bearer " + key

    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 1:  # rate limited: wait as told, then retry once
                time.sleep(int(e.headers.get("Retry-After", "5")))
                continue
            try:
                err = json.load(e)["error"]
                message = f"{e.code} {err.get('code')}: {err.get('message')}"
            except (ValueError, KeyError, TypeError):
                message = f"HTTP {e.code} for {path}"
            raise TaruthaError(message) from None
