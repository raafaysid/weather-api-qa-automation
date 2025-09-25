import requests

def get_response(url, params=None, timeout=10):
    """Reusable GET request helper with a sensible timeout."""
    return requests.get(url, params=params, timeout=timeout)

