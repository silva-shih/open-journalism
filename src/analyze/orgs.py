from __future__ import annotations

import click
import pandas as pd
from rich import print

from src import settings


@click.command()
def orgs():
    """Analyze the organizations."""
    # Load the data
    repo_df = pd.read_csv(
        settings.TRANSFORM_DIR / "org-repos.csv", parse_dates=["updated_at"]
    )

    # Filter out all the forks
    filtered_df = repo_df[~repo_df.fork].copy()

    # Group by the organization, count the number of repos and list the latest update
    org_df = filtered_df.groupby("org").agg(
        repo_count=pd.NamedAgg(column="name", aggfunc="count"),
        stargazers_count=pd.NamedAgg(column="stargazers_count", aggfunc="sum"),
        latest_update=pd.NamedAgg(column="updated_at", aggfunc="max"),
    )

    # Write out the data
    print(f"Writing out org report to {settings.TRANSFORM_DIR / 'org-report.csv'}")
    org_df.to_csv(settings.TRANSFORM_DIR / "org-report.csv")
