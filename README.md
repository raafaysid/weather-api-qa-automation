# Weather API QA Automation Suite

Automated test suite for the OpenWeather REST API using Python + Pytest.

## Features
- Positive and negative tests
- Field/schema validation
- Response time checks
- Parameterized city testing

## Setup
git clone <repo-link>
cd api_automation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENWEATHER_API_KEY="your_api_key"
pytest -v
