from fastmcp import FastMCP
import os
import requests

app = FastMCP(name="github-tools", instructions="GitHub API integration for repository information")

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

def get_headers():
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers

@app.tool(description="Get information about a GitHub repository")
def get_repo_info(owner: str, repo: str):
    """Get basic information about a GitHub repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, headers=get_headers())
    
    if response.status_code != 200:
        return {"error": f"Failed to fetch repository: {response.status_code}"}
    
    data = response.json()
    return {
        "name": data.get("name"),
        "full_name": data.get("full_name"),
        "description": data.get("description"),
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "language": data.get("language"),
        "url": data.get("html_url"),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at")
    }

@app.tool(description="List recent issues for a GitHub repository")
def list_issues(owner: str, repo: str, state: str = "open", limit: int = 10):
    """List issues from a GitHub repository."""
    limit = max(1, min(limit, 100))
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {"state": state, "per_page": limit}
    response = requests.get(url, headers=get_headers(), params=params)
    
    if response.status_code != 200:
        return {"error": f"Failed to fetch issues: {response.status_code}"}
    
    issues = response.json()
    return {
        "count": len(issues),
        "issues": [
            {
                "number": issue.get("number"),
                "title": issue.get("title"),
                "state": issue.get("state"),
                "user": issue.get("user", {}).get("login"),
                "created_at": issue.get("created_at"),
                "url": issue.get("html_url")
            }
            for issue in issues
        ]
    }

@app.tool(description="Search GitHub repositories")
def search_repos(query: str, limit: int = 10):
    """Search for GitHub repositories."""
    limit = max(1, min(limit, 100))
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "per_page": limit, "sort": "stars"}
    response = requests.get(url, headers=get_headers(), params=params)
    
    if response.status_code != 200:
        return {"error": f"Failed to search repositories: {response.status_code}"}
    
    data = response.json()
    return {
        "total_count": data.get("total_count"),
        "repositories": [
            {
                "name": repo.get("name"),
                "full_name": repo.get("full_name"),
                "description": repo.get("description"),
                "stars": repo.get("stargazers_count"),
                "language": repo.get("language"),
                "url": repo.get("html_url")
            }
            for repo in data.get("items", [])
        ]
    }

if __name__ == "__main__":
    app.run()
