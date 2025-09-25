import pytest
from jsonschema import validate
from utils.helpers import get_response
from utils.schemas import github_user_schema

BASE = "https://api.github.com"


@pytest.mark.functional
def test_valid_user_returns_profile():
    """GH-001"""
    r = get_response(f"{BASE}/users/octocat")
    assert r.status_code == 200
    assert r.json().get("login") == "octocat"


@pytest.mark.negative
def test_unknown_user_returns_404():
    """GH-002"""
    r = get_response(f"{BASE}/users/__no_user__")
    assert r.status_code == 404


@pytest.mark.contract
def test_user_response_has_core_fields():
    """GH-003"""
    r = get_response(f"{BASE}/users/torvalds")
    assert r.status_code == 200
    validate(instance=r.json(), schema=github_user_schema)


@pytest.mark.contract
def test_rate_limit_headers_present():
    """GH-004"""
    r = get_response(f"{BASE}/users/octocat")
    assert "X-RateLimit-Limit" in r.headers
    assert "X-RateLimit-Remaining" in r.headers


@pytest.mark.performance
def test_response_time_under_1s():
    """GH-005"""
    r = get_response(f"{BASE}/users/octocat")
    assert r.status_code == 200
    assert r.elapsed.total_seconds() < 1.0


@pytest.mark.functional
def test_pagination_limit_respected():
    """GH-006"""
    r = get_response(f"{BASE}/users/octocat/repos?per_page=5&page=1")
    assert r.status_code == 200
    assert len(r.json()) <= 5
