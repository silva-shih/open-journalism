import os
import json
import time

import click
import pandas as pd
from rich import print
from rich.progress import track
from github import Github, UnknownObjectException

from src import settings


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
    default=1.0,
    help="Number of seconds to wait between requests.",
)
def org_repo_contributors(force: bool = False, wait: float = 1) -> None:
    """Download the contributors for each organization's repos."""
    # Read in our source CSV
    repo_df = pd.read_csv(settings.TRANSFORM_DIR / "org-repos.csv")

    # Filter out forks
    filtered_df = repo_df[~repo_df.fork].copy()
    print(
        f"Downloading contributors for {len(filtered_df)} github repositories linked to newsroom orgs."
    )

    # Loop through the organizations
    contributor_list = []
    for full_name in track(list(filtered_df.full_name), None):
        contributor_list += get_repo_contributors(full_name, force=force, wait=wait)

    # Convert to a dataframe
    contributor_df = pd.DataFrame(contributor_list).sort_values(
        ["org", "repo_name", "login"]
    )

    # Write it out
    contributor_df.to_csv(
        settings.TRANSFORM_DIR / "org-repo-contributors.csv", index=False
    )


def get_repo_contributors(
    full_name: str, force: bool = False, wait: float = 1.0
) -> list[dict]:
    """Get the contributors to a given repository.

    Args:
        full_name: the name of the repository
        force: If True, force the download
        wait: Number of seconds to wait between requests

    Returns:
        A list of dictionaries with the member information.
    """
    # Skip it if we already have the file
    data_path = settings.EXTRACT_DIR / "org-repo-contributors" / f"{full_name}.json"
    data_path.parent.mkdir(exist_ok=True, parents=True)
    if data_path.exists() and not force:
        return json.load(open(data_path))

    # Login to GitHub
    g = Github(os.getenv("GITHUB_API_TOKEN"))

    # Try to get the contributors
    print(f"Downloading contributors for {full_name}")
    try:
        contributors = g.get_repo(full_name).get_contributors()
    except UnknownObjectException:
        contributors = []

    # Parse out each contributor
    d_list = []
    for c in contributors:
        org, repo_name = full_name.split("/")
        assert org and repo_name
        d = dict(
            org=org,
            repo_name=repo_name,
            full_name=full_name,
            id=c.id,
            login=c.login,
            user_name=c.name,
            contributions=c.contributions,
        )
        d_list.append(d)

    # Write it out
    with open(data_path, "w") as fp:
        json.dump(d_list, fp, indent=2)

    # Wait a bit
    time.sleep(wait)

    # Return the data
    return d_list
