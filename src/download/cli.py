import click

from .org_repos import org_repos
from .org_members import org_members
from .org_repo_contributors import org_repo_contributors


@click.group()
def download():
    """Download our data."""
    pass


download.add_command(org_repos)
download.add_command(org_members)
download.add_command(org_repo_contributors)
