"""Check for firmware/OS updates via GitHub releases."""
import json
import os
import urllib.error
import urllib.request

from config import REPO_ROOT, FIRMWARE_REPOS_FOR_UPDATES

GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/releases/latest"
TIMEOUT = 10


def fetch_latest_release(owner: str, repo: str):
    url = GITHUB_API.format(owner=owner, repo=repo)
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read().decode())
            return {
                "tag": data.get("tag_name", ""),
                "name": data.get("name") or data.get("tag_name", ""),
                "url": data.get("html_url", ""),
                "published": data.get("published_at", ""),
            }
    except (urllib.error.HTTPError, urllib.error.URLError, OSError, json.JSONDecodeError) as e:
        return {"error": str(e), "tag": "", "url": ""}


def get_updates():
    """Return list of { name, device, tag, url, error? } for each configured repo."""
    results = []
    for entry in FIRMWARE_REPOS_FOR_UPDATES:
        owner = entry["owner"]
        repo = entry["repo"]
        name = entry.get("name", repo)
        device = entry.get("device", "")
        info = fetch_latest_release(owner, repo)
        results.append({
            "name": name,
            "device": device,
            "repo": f"{owner}/{repo}",
            "tag": info.get("tag", ""),
            "release_name": info.get("name", ""),
            "url": info.get("url", ""),
            "published": info.get("published", ""),
            "error": info.get("error"),
        })
    return results
