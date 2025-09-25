import os
import requests
import pytest
from jsonschema import validate

pytestmark = pytest.mark.skipif(
    not os.getenv("OPENWEATHER_API_KEY"),
    reason="OPENWEATHER_API_KEY not set, skipping live API tests"
)
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")  
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@pytest.mark.functional
def test_weather_api_status_code():
    "Positive: valid city should return 200 OK."
    assert API_KEY, "Set OPENWEATHER_API_KEY in your environment"
    params = {"q": "Tokyo", "appid": API_KEY}
    r = requests.get(BASE_URL, params=params, timeout=10)
    assert r.status_code == 200

@pytest.mark.negative
def test_weather_api_invalid_city():
    "Negative: invalid city should return 404."
    assert API_KEY, "Set OPENWEATHER_API_KEY in your environment"
    params = {"q": "NotARealCity123", "appid": API_KEY}
    r = requests.get(BASE_URL, params=params, timeout=10)
    assert r.status_code == 404
    
@pytest.mark.functional
def test_weather_api_contains_expected_fields():
    assert API_KEY, "Set OPENWEATHER_API_KEY in your environment"
    params = {"q":"London","appid":API_KEY}
    r = requests.get(BASE_URL,params=params,timeout =10)
    assert r.status_code == 200
    data = r.json()
    assert data.get("name").lower() == "london"
    #checking these sections exist
    assert "main" in data       # holds temperature, pressure, humidity
    assert "weather" in data    # holds weather conditions 
    assert "wind" in data       # holds wind speed/direction

@pytest.mark.functional
@pytest.mark.parametrize("city", ["London", "Paris", "New York", "Tokyo", "Houston"])
def test_weather_multiple_cities_return_expected(city):
    """""
    Run the same assertions for multiple cities
    """""
    assert API_KEY, "Set OPENWEATHER_API_KEY in your environment"

    r = requests.get(BASE_URL, params={"q": city, "appid": API_KEY}, timeout=10)

    assert r.status_code == 200

    data = r.json()

    returned = (data.get("name") or "").lower()
    # allowing multi-word names like "New York"
    expected_tokens = city.lower().split()
    assert any(tok in returned for tok in expected_tokens), f"Expected city {city}, got {data.get('name')}"

    # 3) checking core existing questions
    assert "main" in data and "temp" in data["main"]
    assert "weather" in data and isinstance(data["weather"], list) and len(data["weather"]) >= 1

@pytest.mark.contract
def test_weather_response_schema():
    """
    Contract test: the response must have required keys with expected types.
    Catches backend changes that status-code tests might miss.
    """
    assert API_KEY, "Set OPENWEATHER_API_KEY in your environment"
    params = {"q": "London","appid":API_KEY}
    r = requests.get(BASE_URL,params = params, timeout = 10)
    assert r.status_code == 200
    data = r.json()

    # minimal, practical schema
    schema = {
        "type": "object",
        "required": ["name", "coord", "weather", "main"],
        "properties": {
            "name": {"type": "string"},
            "coord": {
                "type": "object",
                "required": ["lon", "lat"],
                "properties": {
                    "lon": {"type": "number"},
                    "lat": {"type": "number"}
                },
                "additionalProperties": True
            },
            "weather": {
                "type": "array",
                "minItems": 1,
                "items": {"type": "object"}
            },
            "main": {
                "type": "object",
                "required": ["temp"],
                "properties": {
                    "temp": {"type": "number"}
                },
                "additionalProperties": True
            },
            "wind": {
                "type": "object",
                "properties": {
                    "speed": {"type": "number"}
                },
                "additionalProperties": True
            }
        },
        # allow backend to add more fields without breakage
        "additionalProperties": True
    }

    #will raise a ValidationError (and fail the test) if the shape is wrong
    validate(instance=data, schema=schema)

@pytest.mark.performance
def test_weather_response_time_under_1_5s():
    assert API_KEY, "Set OPENWEATHER_API_KEY in your environment"
    params = {"q":"London","appid":API_KEY}
    r = requests.get(BASE_URL,params = params, timeout = 10)
    assert r.status_code == 200

    elapsed = r.elapsed.total_seconds()
    assert elapsed < 1.0, f"Response too slow: {elapsed:.3f}s (expected < 1.5s)"
