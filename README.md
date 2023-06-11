# FSPy
An easy to use FlareSolverr wrapper for Python.

## Usage
```python
from fspy import FlareSolverr

solver = FlareSolverr()

# With custom ip and port
solver = FlareSolverr(host="127.0.0.1", port="5050")

# With https
solver = FlareSolverr(http_schema="https")

# If you want some additional headers
headers = {
    "Connection": "keep-alive"
}
solver = FlareSolverr(additional_headers=headers)

# When (for whatever the reason) flaresolverr changes /v1 endpoint
solver = FlareSolverr(v="v2")

# List all session ids
sessions = solver.sessions

# List sessions response
sessions = solver._sessions_raw

# Create a session with a random UUID
new_session = solver.create_session()

# Create a session with a custom id and proxy
new_session = solver.create_session(session_id="thisismyid", proxy_url="http://thisismycustomproxyurl.uwu")

# Delete a session
response = solver.destroy_session("thisismyid")

# Get request
response = solver.request_get("https://google.com")
# All flaresolverr additional args are supported

# Post request
params = {
    "param1": "value1",
    "param2": 2,
    "param3": [3, 3, 3]
}
response = solver.request_post("https://google.com", params)

```