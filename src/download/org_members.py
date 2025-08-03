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
def org_members(force: bool = False, wait: float = 1.0) -> None:
    """Download the members of each organization."""
    # Read in our source CSV
    org_df = pd.read_csv(settings.ROOT_DIR / "orgs.csv")
    print(f"Downloading members for {len(org_df)} github organizations.")

    # Parse out the github handles
    org_df["handle"] = org_df["Github"].apply(
        lambda x: x.split("/")[-1].lower().strip()
    )

    # Loop through the organizations
    member_list = []
    for org in track(list(org_df.handle), None):
        member_list += get_org_members(org, force=force, wait=wait)

    # Convert to a dataframe
    member_df = pd.DataFrame(member_list).sort_values(["org", "login"])

    # Write it out
    member_df.to_csv(settings.TRANSFORM_DIR / "org-members.csv", index=False)


def get_org_members(org: str, force: bool = False, wait: float = 1.0) -> list[dict]:
    """Get the members for a given org.

    Args:
        org: The organization or user to download.
        force: If True, force the download.
        wait: Number of seconds to wait between requests.

    Returns:
        A list of dictionaries with the member information.
    """
    # Skip it if we already have the file
    data_path = settings.EXTRACT_DIR / "org-members" / f"{org}.json"
    data_path.parent.mkdir(exist_ok=True, parents=True)
    if data_path.exists() and not force:
        return json.load(open(data_path))

    # Login to GitHub
    g = Github(os.getenv("GITHUB_API_TOKEN"))

    # Try to download an org
    print(f"Downloading {org} members")
    try:
        members = g.get_organization(org).get_members()
    except UnknownObjectException:
        members = []

    # Parse out each member
    d_list = []
    for m in members:
        d = dict(
            org=org,
            id=m.id,
            login=m.login,
            name=m.name,
            created_at=str(m.created_at),
            updated_at=str(m.updated_at),
        )
        d_list.append(d)

    # Write it out
    with open(data_path, "w") as fp:
        json.dump(d_list, fp, indent=2)

    # Wait a bit
    time.sleep(wait)

    # Return the data
    return d_list
