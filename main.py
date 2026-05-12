import click

from services.dev_v1_service import command as dev_v1
from services.test_v1_service import command as test_v1
from services.main_service import command as main_branch
from services.copy_build_service import command as copy_build


@click.group()
def cli():
    """Frontend Automation — pull and build by branch."""


# ── Register routes ─────────────────────────────────────────────────────────

cli.add_command(dev_v1)
cli.add_command(test_v1)
cli.add_command(main_branch)
cli.add_command(copy_build)


if __name__ == "__main__":
    cli()
