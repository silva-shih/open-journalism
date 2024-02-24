"""Download repos for analysis."""
from __future__ import annotations

import os
import json
import time
from pathlib import Path

from github import Github
from github import UnknownObjectException

import click
import pandas as pd
from rich import print
from rich.progress import track

THIS_DIR = Path(__file__).parent


@click.command()
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Force the download of the data.",
)
@click.option(
    "-w",
    "--wait",
    default=1,
    help="Number of seconds to wait between requests.",
)
def cli(force: bool, wait: int) -> None:
    """Download repos for analysis."""
    # Read in our source CSV
    org_df = pd.read_csv(THIS_DIR / "orgs.csv")

    # Parse out the github handles
    org_df['handle'] = org_df['Github'].apply(lambda x: x.split("/")[-1].lower().strip())

    # Assert that none of the handles are empty strings
    try:
        assert not any(org_df.handle == "")
    except AssertionError:
        empty_handles = org_df[org_df.handle == ""].Github.unique()
        print(f"Empty handles: {empty_handles}")
        raise

    # Assert that there are no duplicate handles
    try:
        assert not org_df.handle.duplicated().any()
    except AssertionError:
        dupes = org_df[org_df.handle.duplicated()].handle.unique()
        print(f"Duplicate handles: {dupes}")
        raise

    # Loop through the repositories
    repo_list = []
    for org in track(list(org_df.handle)):
        repo_list += get_repo_list(org, force=force, wait=wait)

    # Convert to a dataframe
    repo_df = pd.DataFrame(repo_list).sort_values(["org", "name"])

    # Create the output directory
    repo_df.to_csv(THIS_DIR / "repos.csv", index=False)


def get_repo_list(org: str, force: bool = False, wait: int = 1) -> list[dict]:
    """Get the repos for a given org.

    Args:
        org: The organization or user to download.
        force: If True, force the download.
        wait: Number of seconds to wait between requests.

    Returns:
        A list of dictionaries with the repo information.
    """
    # Skip it if we already have the file
    data_path = THIS_DIR / "data" / f"{org}.json"
    data_path.parent.mkdir(exist_ok=True, parents=True)
    if data_path.exists() and not force:
        return json.load(open(data_path, 'r'))

    # Login to GitHub
    g = Github(os.getenv("GITHUB_API_TOKEN"))

    # Try to download an org
    print(f"Downloading {org}")
    try:
        repo_list = g.get_organization(org).get_repos()
    except UnknownObjectException:
        try:
            # Try to download a user
            repo_list = g.get_user(org).get_repos()
        except UnknownObjectException:
            # Give up
            return []

    def _get_license(r):
       return r.license.name if r.license else None
    
    # Parse out each repo and when it was created    
    d_list = []
    for r in repo_list:
        d = dict(
            org=org,
            name=r.name,
            full_name=r.full_name,
            homepage=r.homepage,
            description=r.description,
            language=r.language,
            created_at=str(r.created_at),
            updated_at=str(r.updated_at),
            pushed_at=str(r.pushed_at),
            fork=r.fork,
            stargazers_count=r.stargazers_count,
            watchers_count=r.watchers_count,
            forks_count=r.forks_count,
            open_issues_count=r.open_issues_count,
            license=_get_license(r),
            topics=r.topics,
        )
        d_list.append(d)

    # Write it out
    with open(data_path, "w") as fp:
        json.dump(d_list, fp, indent=2)

    # Wait a bit
    time.sleep(wait)

    # Return the data
    return d_list


if __name__ == "__main__":
    cli()