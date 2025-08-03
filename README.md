Analyzing open-source journalism projects on GitHub

The list of news-related organizations maintained at [repo.csv](repos.csv) serves as the basis for our work. If you know of a news organization posting code that we're missing, please file an issue.

## Installation

The Python dependencies are installed with the `uv` package manager.

```bash
uv sync
```

Create [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) with GitHub that will allow you access to the metadata and commit history of public repositories.

Set that token to your terminal's environment as the `GITHUB_API_TOKEN` variable. This can be done with a `.env` file or another environment management tool.

Reset the downloaded data folder. Only do this if you want to wipe everything. A full download will take a while.

```bash
make clean
```

Download the latest data from organization's profile.

```bash
make download
```

Analyze the result.

```bash
make analyze
```
