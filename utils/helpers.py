import os
import requests

def get_response(url, params=None, timeout=10):
    """
    Reusable GET with sensible defaults
    - Always sends a UserAgent (GitHub requires it)
    - If hitting api.github.com and a token is present, auth to avoid rate limits
    """
    headers = {"User-Agent": "weather-api-qa-suite/1.0"}

    if "api.github.com" in url:
        token = os.getenv("GITHUB_API_TOKEN") or os.getenv("GITHUB_TOKEN")
        # ^ allow either a custom secret or the built in GITHUB_TOKEN
        headers["Accept"] = "application/vnd.github+json"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
        if token:
            headers["Authorization"] = f"Bearer {token}"

    return requests.get(url, params=params, timeout=timeout, headers=headers)
