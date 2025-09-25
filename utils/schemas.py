# utils/schemas.py

# Minimal contract we care about for Weather
weather_schema = {
    "type": "object",
    "required": ["name", "main", "weather", "wind"],
    "properties": {
        "name": {"type": "string"},
        "main": {
            "type": "object",
            "required": ["temp"],
            "properties": {"temp": {"type": "number"}}
        },
        "weather": {"type": "array"},
        "wind": {"type": "object"}
    }
}

# Minimal contract for GitHub user
github_user_schema = {
    "type": "object",
    "required": ["login", "id", "public_repos"],
    "properties": {
        "login": {"type": "string"},
        "id": {"type": "number"},
        "public_repos": {"type": "number"}
    }
}

