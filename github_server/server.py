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

@app.tool(description="Create a new branch in a repository")
def create_branch(owner: str, repo: str, branch_name: str, from_branch: str = "main"):
    """Create a new branch from an existing branch."""
    # Get the SHA of the source branch
    url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{from_branch}"
    response = requests.get(url, headers=get_headers())
    
    if response.status_code != 200:
        return {"error": f"Failed to get source branch: {response.status_code}", "message": response.text}
    
    sha = response.json()["object"]["sha"]
    
    # Create new branch
    url = f"https://api.github.com/repos/{owner}/{repo}/git/refs"
    data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": sha
    }
    response = requests.post(url, headers=get_headers(), json=data)
    
    if response.status_code == 201:
        return {
            "success": True,
            "branch": branch_name,
            "sha": sha,
            "message": f"Branch '{branch_name}' created successfully"
        }
    else:
        return {"error": f"Failed to create branch: {response.status_code}", "message": response.text}

@app.tool(description="Create or update a file in a repository")
def create_or_update_file(owner: str, repo: str, path: str, content: str, message: str, branch: str, sha: str = None):
    """Create or update a file in a repository. If sha is provided, it updates the file; otherwise creates new."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    # Encode content to base64
    import base64
    content_encoded = base64.b64encode(content.encode()).decode()
    
    data = {
        "message": message,
        "content": content_encoded,
        "branch": branch
    }
    
    if sha:
        data["sha"] = sha
    
    response = requests.put(url, headers=get_headers(), json=data)
    
    if response.status_code in [200, 201]:
        result = response.json()
        return {
            "success": True,
            "path": path,
            "sha": result["content"]["sha"],
            "message": f"File '{path}' {'updated' if sha else 'created'} successfully"
        }
    else:
        return {"error": f"Failed to create/update file: {response.status_code}", "message": response.text}

@app.tool(description="Get file content from a repository")
def get_file_content(owner: str, repo: str, path: str, branch: str = "main"):
    """Get the content of a file from a repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    params = {"ref": branch}
    response = requests.get(url, headers=get_headers(), params=params)
    
    if response.status_code != 200:
        return {"error": f"Failed to get file: {response.status_code}", "message": response.text}
    
    data = response.json()
    
    # Decode content from base64
    import base64
    content = base64.b64decode(data["content"]).decode()
    
    return {
        "path": data["path"],
        "sha": data["sha"],
        "content": content,
        "size": data["size"]
    }

@app.tool(description="Create a pull request")
def create_pull_request(owner: str, repo: str, title: str, head: str, base: str = "main", body: str = ""):
    """Create a pull request from head branch to base branch."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    data = {
        "title": title,
        "head": head,
        "base": base,
        "body": body
    }
    
    response = requests.post(url, headers=get_headers(), json=data)
    
    if response.status_code == 201:
        pr = response.json()
        return {
            "success": True,
            "number": pr["number"],
            "title": pr["title"],
            "url": pr["html_url"],
            "state": pr["state"],
            "created_at": pr["created_at"]
        }
    else:
        return {"error": f"Failed to create PR: {response.status_code}", "message": response.text}

@app.tool(description="List branches in a repository")
def list_branches(owner: str, repo: str, limit: int = 30):
    """List branches in a repository."""
    limit = max(1, min(limit, 100))
    url = f"https://api.github.com/repos/{owner}/{repo}/branches"
    params = {"per_page": limit}
    response = requests.get(url, headers=get_headers(), params=params)
    
    if response.status_code != 200:
        return {"error": f"Failed to list branches: {response.status_code}"}
    
    branches = response.json()
    return {
        "count": len(branches),
        "branches": [
            {
                "name": branch["name"],
                "sha": branch["commit"]["sha"],
                "protected": branch.get("protected", False)
            }
            for branch in branches
        ]
    }

if __name__ == "__main__":
    app.run()
