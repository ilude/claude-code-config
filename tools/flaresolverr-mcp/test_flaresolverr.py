#!/usr/bin/env python3
"""Quick test of FlareSolverr API."""
import requests
import json

api_url = "http://localhost:8191/v1"
test_url = "https://platform.openai.com/docs"

print(f"Testing FlareSolverr with: {test_url}")
print("Creating session...")

# Create session
response = requests.post(api_url, json={"cmd": "sessions.create"})
data = response.json()
session_id = data.get("session")
print(f"Session ID: {session_id}")

print(f"\nFetching {test_url}...")
print("(This may take 15-30 seconds to solve Cloudflare challenge...)")

# Solve challenge
response = requests.post(
    api_url,
    json={
        "cmd": "request.get",
        "url": test_url,
        "maxTimeout": 60000,
        "session": session_id
    },
    timeout=70
)

data = response.json()
if data.get("status") == "ok":
    solution = data.get("solution", {})
    print(f"\n[SUCCESS]")
    print(f"Status: {solution.get('status')}")
    print(f"URL: {solution.get('url')}")
    print(f"User-Agent: {solution.get('userAgent')}")
    print(f"Cookies: {len(solution.get('cookies', []))} cookies")
    print(f"HTML length: {len(solution.get('response', ''))} chars")
    print(f"\nFirst 500 chars of HTML:")
    print(solution.get('response', '')[:500])
else:
    print(f"\n[FAILED]: {data.get('message')}")

# Cleanup
print("\nCleaning up session...")
requests.post(api_url, json={"cmd": "sessions.destroy", "session": session_id})
print("Done!")
