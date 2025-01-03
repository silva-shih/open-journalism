import requests
import csv

# Constants
github_account = "Automattic"
repo_prefix = "newspack-"
output_file = "newspack_repos.csv"

def fetch_repos(account):
    url = f"https://api.github.com/users/{account}/repos"
    repos = []
    page = 1

    while True:
        response = requests.get(url, params={"per_page": 100, "page": page})
        if response.status_code != 200:
            print(f"Error: Unable to fetch repositories (status code {response.status_code})")
            break

        data = response.json()
        if not data:
            break

        repos.extend(data)
        page += 1

    return repos

def filter_repos(repos, prefix):
    return [
        {
            "name": repo["name"],
            "created_at": repo["created_at"]
        }
        for repo in repos if repo["name"].startswith(prefix)
    ]

def write_to_csv(repos, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Repository Name", "Creation Date"])
        for repo in repos:
            writer.writerow([repo["name"], repo["created_at"]])

def main():
    print(f"Fetching repositories for account: {github_account}...")
    repos = fetch_repos(github_account)

    print(f"Filtering repositories with prefix: {repo_prefix}...")
    filtered_repos = filter_repos(repos, repo_prefix)

    print(f"Writing results to {output_file}...")
    write_to_csv(filtered_repos, output_file)

    print(f"Done! Results saved to {output_file}")

if __name__ == "__main__":
    main()
