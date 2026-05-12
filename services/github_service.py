import json

import requests

from config import DEV_BRANCH, GITHUB_API_BASE, GITHUB_REPO, GITHUB_TOKEN, MAIN_BRANCH

_HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def get_recent_commits() -> str:
    url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/commits?sha={DEV_BRANCH}&per_page=10"
    resp = requests.get(url, headers=_HEADERS, timeout=30)
    resp.raise_for_status()

    return json.dumps(
        [
            {
                "sha": c["sha"][:7],
                "message": c["commit"]["message"].split("\n")[0],
                "author": c["commit"]["author"]["name"],
                "date": c["commit"]["author"]["date"][:10],
            }
            for c in resp.json()
        ]
    )


def check_existing_prs() -> str:
    owner = GITHUB_REPO.split("/")[0]
    url = (
        f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/pulls"
        f"?state=open&head={owner}:{DEV_BRANCH}&base={MAIN_BRANCH}"
    )
    resp = requests.get(url, headers=_HEADERS, timeout=30)
    resp.raise_for_status()

    prs = resp.json()
    if not prs:
        return "no_open_prs"

    return json.dumps(
        [{"number": p["number"], "title": p["title"], "url": p["html_url"]} for p in prs]
    )


def create_pull_request(title: str, body: str) -> str:
    url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/pulls"
    payload = {
        "title": title,
        "body": body,
        "head": DEV_BRANCH,
        "base": MAIN_BRANCH,
        "draft": False,
    }
    resp = requests.post(url, headers=_HEADERS, json=payload, timeout=30)

    if resp.status_code == 422:
        errors = resp.json().get("errors", [])
        if any("already exists" in str(e) for e in errors):
            return "pr_already_exists: an open PR from dev→main already exists"
        return f"validation_error: {resp.json()}"

    resp.raise_for_status()
    pr = resp.json()
    return json.dumps(
        {
            "status": "created",
            "pr_number": pr["number"],
            "url": pr["html_url"],
            "title": pr["title"],
        }
    )
