from collections import defaultdict
from datetime import datetime
import requests
import time


def GetCommits():
    req = {
        "repositories": [
            {
                "url": "https://github.com/mershab99/CTCI"
            },
            {
                "url": "https://github.com/mershab99/website"
            },
            {
                "url": "https://gitlab.com/syntaxandsoul/medconsent/poc",
            }
        ],
        "days": 180
    }
    res = requests.post("http://localhost:8080/commits", json=req)
    return res.json()

def GetHeatmapData(commit_data: dict):
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
