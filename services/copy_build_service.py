import shutil
import sys
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

from config import DEPLOY_PATH, PROJECT_PATH

console = Console()

BUILD_DIR = PROJECT_PATH / "dist"


def copy_build(destination: Path = DEPLOY_PATH) -> dict:
    if not BUILD_DIR.exists():
        return {
            "status": "failed",
            "detail": f"Build folder not found: {BUILD_DIR}. Run a build first.",
        }

    dest = Path(destination) / "dist"

    if dest.exists():
        shutil.rmtree(dest)

    shutil.copytree(str(BUILD_DIR), str(dest))

    files_copied = sum(1 for _ in dest.rglob("*") if _.is_file())

    return {
        "status": "success",
        "source": str(BUILD_DIR),
        "destination": str(dest),
        "files_copied": files_copied,
        "copied_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


@click.command(name="copy-build")
@click.option("--dest", default=str(DEPLOY_PATH), help="Destination path to copy build into.")
def command(dest: str):
    """Copy the dist/ build folder to a target path."""
    console.print(Panel.fit("[bold cyan]Copy Build[/bold cyan]", title="Starting"))
    console.print(f"[cyan]Source:[/cyan]      {BUILD_DIR}")
    console.print(f"[cyan]Destination:[/cyan] {dest}")

    result = copy_build(Path(dest))

    if result["status"] == "success":
        console.print(Panel(
            f"Copied {result['files_copied']} files\n"
            f"From : {result['source']}\n"
            f"To   : {result['destination']}\n"
            f"At   : {result['copied_at']}",
            title="[green]Done[/green]",
            border_style="green",
        ))
    else:
        console.print(Panel(result["detail"], title="[red]Failed[/red]", border_style="red"))
        sys.exit(1)


if __name__ == "__main__":
    command()
