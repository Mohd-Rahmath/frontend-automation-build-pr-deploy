import json
import subprocess

import requests

from config import DEV_BRANCH, GITHUB_API_BASE, GITHUB_REPO, GITHUB_TOKEN, PROJECT_PATH
from services import state_service

_HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def check_new_commits() -> str:
    last_sha = state_service.get_last_sha()

    url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/commits?sha={DEV_BRANCH}&per_page=10"
    resp = requests.get(url, headers=_HEADERS, timeout=30)
    resp.raise_for_status()

    commits = resp.json()
    if not commits:
        return "no_commits_found"

    latest_sha = commits[0]["sha"]
    if latest_sha == last_sha:
        return "no_new_commits"

    new_commits = []
    for c in commits:
        if c["sha"] == last_sha:
            break
        new_commits.append(
            {
                "sha": c["sha"][:7],
                "message": c["commit"]["message"].split("\n")[0],
                "author": c["commit"]["author"]["name"],
                "date": c["commit"]["author"]["date"][:10],
            }
        )

    return json.dumps(
        {"latest_sha": latest_sha, "new_commits": new_commits, "count": len(new_commits)}
    )


def pull_dev_branch() -> str:
    try:
        for cmd in [
            ["git", "fetch", "origin"],
            ["git", "checkout", DEV_BRANCH],
            ["git", "pull", "origin", DEV_BRANCH],
        ]:
            result = subprocess.run(
                cmd, cwd=str(PROJECT_PATH), capture_output=True, text=True, timeout=60
            )
            if result.returncode != 0:
                return f"failed at '{' '.join(cmd)}': {result.stderr.strip()}"

        return f"success: pulled latest {DEV_BRANCH}"
    except subprocess.TimeoutExpired:
        return "error: git operation timed out"
    except Exception as exc:
        return f"error: {exc}"
