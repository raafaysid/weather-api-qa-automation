# API Test Plan

## Overview
This suite covers two public APIs:  
- **OpenWeather** for weather data  
- **GitHub Users** for profile info  

The goal is to check that both work as expected with good input, handle bad input properly, and return the fields and speed we’d expect.  
Below are the main scenarios I designed before automating them.

---

## OpenWeather API

| ID     | Scenario | Why it matters | Steps | What I expect |
|--------|----------|----------------|-------|---------------|
| OW-001 | Valid city returns 200 | Make sure basic functionality works | Call `?q=Tokyo&appid=KEY` | 200 OK + JSON body with Tokyo’s info |
| OW-002 | Fake city returns 404 | Handle user mistakes gracefully | Call `?q=NotARealCity123&appid=KEY` | 404 with a clear error message |
| OW-003 | Response has core fields | Weather data should be usable | Call `?q=London&appid=KEY` | JSON includes `main.temp`, `weather[]`, `wind` |
| OW-004 | Multiple cities behave the same | Consistency across inputs | Try London, Paris, NY, Tokyo, Houston | 200 OK each, with `name` matching city |
| OW-005 | Invalid/missing key blocked | Security check | Call without key or with bad key | 401 Unauthorized |
| OW-006 | Response is reasonably fast | User experience | Call valid city | Response < ~1.5s |

---

## GitHub Users API

| ID     | Scenario | Why it matters | Steps | What I expect |
|--------|----------|----------------|-------|---------------|
| GH-001 | Valid user returns profile | Core functionality | `GET /users/octocat` | 200 OK + JSON with `login="octocat"` |
| GH-002 | Unknown user returns 404 | Bad input handled cleanly | `GET /users/__no_user__` | 404 with error JSON |
| GH-003 | Response has core fields | Contract check | `GET /users/torvalds` | JSON includes `login`, `id`, `public_repos` |
| GH-004 | Rate limit headers exist | Helps track usage | Any valid user | Response headers include `X-RateLimit-Remaining` |
| GH-005 | Fast enough response | Performance | Any valid user | Response < ~1s |
| GH-006 | Pagination respected | Important for repo listings | `/users/octocat/repos?per_page=5&page=1` | 200 OK, ≤5 items returned |

---

## Notes
- These test cases were drafted first to think through coverage.  
- Each one now maps to an automated Pytest function in the repo.  
- Marks (`@pytest.mark.functional`, `negative`, etc.) link them back to these scenarios.  
- CI runs them automatically on GitHub Actions to keep the suite green.


