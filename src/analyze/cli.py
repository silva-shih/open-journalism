import click

from .new_repos_by_month import new_repos_by_month
from .orgs import orgs


@click.group()
def analyze():
    """Analyze our data."""
    pass


analyze.add_command(new_repos_by_month)
analyze.add_command(orgs)
