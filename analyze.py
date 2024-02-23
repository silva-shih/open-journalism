"""Analyze our data."""
from __future__ import annotations

from pathlib import Path

import click
import pandas as pd
from rich import print

THIS_DIR = Path(__file__).parent


@click.group()
def cli():
    """Analyze our data."""
    pass


@cli.command()
def org_report():
    # Load the data
    repo_df = pd.read_csv(THIS_DIR / "repos.csv", parse_dates=["updated_at"])

    # Filter out all the forks
    filtered_df = repo_df[~repo_df.fork].copy()

    # Group by the organization, count the number of repos and list the latest update
    org_df = filtered_df.groupby("org").agg(
        repo_count=pd.NamedAgg(column="name", aggfunc="count"),
        stargazers_count=pd.NamedAgg(column="stargazers_count", aggfunc="sum"),
        latest_update=pd.NamedAgg(column="updated_at", aggfunc="max"),
    )

    # Write out the data
    org_df.to_csv(THIS_DIR / "org-report.csv")


@cli.command()
def new_repos_by_month():
    """Output the number of new repos by month."""
    # Load the data
    repo_df = pd.read_csv(THIS_DIR / "repos.csv", parse_dates=["created_at"])

    # Group by the organization, count the number of repos and list the latest update
    org_df = repo_df.groupby(
        pd.Grouper(key="created_at", freq="ME")
    ).size().reset_index(name="count")

    # Convert the date to a YYYY-MM format
    org_df["created_at"] = org_df["created_at"].dt.strftime("%Y-%m")

    # Write out the data
    org_df.to_csv(THIS_DIR / "new-repos-by-month.csv", index=False)



if __name__ == "__main__":
    cli()