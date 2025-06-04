from collections import defaultdict
from datetime import datetime
import requests
import json
import os

# Toggle behavior
USE_CACHE = False

# Simple in-memory cache
REQUEST_CACHE_COMMITS = {}
REQUEST_CACHE_HEATMAP = {}

#GIT_REPO_STATS_API_URL = "http://localhost:8080"
GIT_REPO_STATS_API_URL = "https://git-repo-stats.mershab.com"

# Path to request JSON file
REQUEST_FILE_PATH = os.path.join("request.json")


def load_request_data():
    with open(REQUEST_FILE_PATH, "r") as f:
        return json.load(f)

def fetch_commits_heatmap(req):
    key = json.dumps(req, sort_keys=True)

    if USE_CACHE:
        if key not in REQUEST_CACHE_HEATMAP:
            try:
                res = requests.post(f"{GIT_REPO_STATS_API_URL}/commits/heatmap", json=req)
                REQUEST_CACHE_HEATMAP[key] = res
            except Exception:
                res = None
        else:
            res = REQUEST_CACHE_HEATMAP[key]
    else:
        try:
            res = requests.post(f"{GIT_REPO_STATS_API_URL}/commits/heatmap", json=req)
        except Exception:
            res = None

    return res.json() if res else None


def fetch_commits(req):
    key = json.dumps(req, sort_keys=True)

    if USE_CACHE:
        if key not in REQUEST_CACHE_COMMITS:
            try:
                # res = requests.post("https://git-repo-stats.mershab.com/commits", json=req)
                res = requests.post("http://localhost:8080/commits", json=req)
                REQUEST_CACHE_COMMITS[key] = res
            except Exception:
                res = None
        else:
            res = REQUEST_CACHE_COMMITS[key]
    else:
        try:
            res = requests.post("http://localhost:8080/commits", json=req)
        except Exception:
            res = None

    return res.json() if res else None


def get_heatmap_data(commit_data: dict):
    counts = defaultdict(int)

    for git_repo, commits in commit_data.items():
        if commits:
            for commit in commits:
                try:
                    dt = datetime.fromisoformat(commit["timestamp"])
                    date_str = dt.strftime("%Y-%m-%d")
                    counts[date_str] += 1
                except Exception as e:
                    print(f"Skipping malformed commit: {commit} ({e})")

    heatmap_data = [
        {"date": date, "value": count}
        for date, count in sorted(counts.items())
    ]
    print(heatmap_data)
    return heatmap_data
