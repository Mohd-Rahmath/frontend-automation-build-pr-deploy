import json

from langchain_core.tools import tool

from services import build_service, git_service, github_service, state_service


@tool
def check_new_commits_on_dev(dummy: str = "") -> str:
    """Check if the dev branch has new commits since the last automation run."""
    return git_service.check_new_commits()


@tool
def pull_latest_dev_code(dummy: str = "") -> str:
    """Pull the latest code from the dev branch into the local project directory."""
    return git_service.pull_dev_branch()


@tool
def run_frontend_build(dummy: str = "") -> str:
    """Run 'npm run build' in the frontend project directory."""
    return build_service.run_build()


@tool
def check_existing_prs(dummy: str = "") -> str:
    """Check if an open PR from dev to main already exists on GitHub."""
    return github_service.check_existing_prs()


@tool
def get_recent_commits(dummy: str = "") -> str:
    """Fetch the last 10 commits from the dev branch for use in PR descriptions."""
    return github_service.get_recent_commits()


@tool
def create_github_pull_request(title_and_body: str) -> str:
    """Create a GitHub pull request from dev to main.

    Pass a JSON string with keys 'title' (str) and 'body' (str, markdown).
    """
    try:
        data = json.loads(title_and_body)
        return github_service.create_pull_request(data["title"], data["body"])
    except (json.JSONDecodeError, KeyError) as exc:
        return f"input_error: expected JSON with 'title' and 'body' — {exc}"


@tool
def mark_commits_processed(latest_sha: str) -> str:
    """Save the latest processed commit SHA so it is not reprocessed next run."""
    state_service.set_last_sha(latest_sha)
    return f"saved: SHA {latest_sha[:7]} marked as processed"


ALL_TOOLS = [
    check_new_commits_on_dev,
    pull_latest_dev_code,
    run_frontend_build,
    check_existing_prs,
    get_recent_commits,
    create_github_pull_request,
    mark_commits_processed,
]
