import click

from src.download.cli import download as download_cli
from src.analyze.cli import analyze as analyze_cli


@click.group()
def cli_group():
    """Main entry point for the CLI."""
    pass


cli_group.add_command(download_cli)
cli_group.add_command(analyze_cli)
