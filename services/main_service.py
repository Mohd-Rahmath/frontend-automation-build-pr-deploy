import os
import subprocess
import sys

import click
from rich.console import Console
from rich.panel import Panel

from config import PROJECT_PATH

BRANCH = "main"
console = Console()


def pull() -> str:
    try:
        for cmd in [
            ["git", "fetch", "origin"],
            ["git", "checkout", BRANCH],
            ["git", "pull", "origin", BRANCH],
        ]:
            result = subprocess.run(
                cmd, cwd=str(PROJECT_PATH), capture_output=True, text=True, timeout=60
            )
            if result.returncode != 0:
                return f"failed at '{' '.join(cmd)}': {result.stderr.strip()}"
        return f"success: pulled latest {BRANCH}"
    except subprocess.TimeoutExpired:
        return "error: git operation timed out"
    except Exception as exc:
        return f"error: {exc}"


def build() -> dict:
    npm = "npm.cmd" if sys.platform == "win32" else "npm"
    env = {**os.environ, "CI": "false"}
    try:
        result = subprocess.run(
            [npm, "run", "build"],
            cwd=str(PROJECT_PATH),
            capture_output=True,
            text=True,
            timeout=300,
            env=env,
        )
        stdout = result.stdout[-4000:] if len(result.stdout) > 4000 else result.stdout
        stderr = result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr
        if result.returncode == 0:
            return {"status": "success", "output": stdout}
        return {"status": "failed", "output": stdout, "error": stderr}
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "error": "Build timed out after 5 minutes"}
    except Exception as exc:
        return {"status": "error", "error": str(exc)}


@click.command(name="main")
def command():
    """Pull main and run npm run build."""
    console.print(Panel.fit(f"[bold cyan]Branch: {BRANCH}[/bold cyan]", title="Starting"))

    console.print(f"[cyan]Step 1:[/cyan] Pulling [bold]{BRANCH}[/bold]...")
    pull_result = pull()
    console.print(f"  {pull_result}")

    if "failed" in pull_result or "error" in pull_result:
        console.print(Panel(f"Stopped: {pull_result}", title="[red]Failed[/red]", border_style="red"))
        sys.exit(1)

    console.print("[cyan]Step 2:[/cyan] Running [bold]npm run build[/bold]...")
    build_result = build()

    if build_result["status"] == "success":
        console.print("  [green]Build passed.[/green]")
        console.print(Panel(f"Done: pulled {BRANCH} and build succeeded.", title="[green]Done[/green]", border_style="green"))
    else:
        error = build_result.get("error") or build_result.get("output", "")
        console.print(Panel(f"Build failed:\n{error[:500]}", title="[red]Failed[/red]", border_style="red"))
        sys.exit(1)


if __name__ == "__main__":
    command()
