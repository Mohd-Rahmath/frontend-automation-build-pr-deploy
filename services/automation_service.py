import json
import sys

from rich.console import Console

from config import (
    DEV_BRANCH,
    GITHUB_REPO,
    GITHUB_TOKEN,
    MAIN_BRANCH,
    PROJECT_PATH,
)
from services import build_service, git_service

console = Console()


def validate_config() -> None:
    if not GITHUB_TOKEN:
        console.print("[red]Missing required env var:[/red] GITHUB_TOKEN")
        console.print("Copy [bold].env.example[/bold] -> [bold].env[/bold] and fill in your token.")
        sys.exit(1)


def get_banner() -> str:
    return (
        f"[bold cyan]Frontend Automation[/bold cyan]\n"
        f"Repo : [yellow]{GITHUB_REPO}[/yellow]\n"
        f"Flow : [yellow]{DEV_BRANCH}[/yellow] -> [yellow]{MAIN_BRANCH}[/yellow]\n"
        f"Path : {PROJECT_PATH}"
    )


def run_once() -> str:
    # Step 1 — pull Dev-v1
    console.print(f"[cyan]Step 1:[/cyan] Pulling [bold]{DEV_BRANCH}[/bold]...")
    pull_result = git_service.pull_dev_branch()
    console.print(f"  {pull_result}")

    if "failed" in pull_result or "error" in pull_result:
        return f"Stopped at git pull: {pull_result}"

    # Step 2 — npm run build
    console.print("[cyan]Step 2:[/cyan] Running [bold]npm run build[/bold]...")
    build_result = json.loads(build_service.run_build())

    if build_result["status"] == "success":
        console.print("  [green]Build passed.[/green]")
        return "Done: pulled Dev-v1 and build succeeded."
    else:
        error = build_result.get("error") or build_result.get("output", "")
        console.print(f"  [red]Build failed.[/red]\n{error[:500]}")
        return f"Build failed:\n{error[:500]}"
