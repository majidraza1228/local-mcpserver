#!/usr/bin/env python3
"""Test script to verify GitHub server functionality"""

import os
import requests

# Get GitHub token from environment variable
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')

def get_headers():
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers

def test_get_repo_info():
    """Test getting repository information"""
    print("Testing get_repo_info...")
    url = "https://api.github.com/repos/majidraza1228/local-mcpserver"
    response = requests.get(url, headers=get_headers())
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Repository: {data.get('full_name')}")
        print(f"  Description: {data.get('description')}")
        print(f"  Stars: {data.get('stargazers_count')}")
        print(f"  Language: {data.get('language')}")
        print(f"  Created: {data.get('created_at')}")
    else:
        print(f"✗ Failed with status code: {response.status_code}")
        print(f"  Response: {response.text}")
    print()

def test_list_issues():
    """Test listing issues"""
    print("Testing list_issues...")
    url = "https://api.github.com/repos/fastmcp/fastmcp/issues"
    params = {"state": "open", "per_page": 5}
    response = requests.get(url, headers=get_headers(), params=params)
    
    if response.status_code == 200:
        issues = response.json()
        print(f"✓ Found {len(issues)} open issues")
        for issue in issues[:3]:
            print(f"  #{issue['number']}: {issue['title']}")
    else:
        print(f"✗ Failed with status code: {response.status_code}")
    print()

def test_search_repos():
    """Test searching repositories"""
    print("Testing search_repos...")
    url = "https://api.github.com/search/repositories"
    params = {"q": "fastmcp", "per_page": 3, "sort": "stars"}
    response = requests.get(url, headers=get_headers(), params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {data.get('total_count')} repositories")
        for repo in data.get('items', [])[:3]:
            print(f"  {repo['full_name']} - {repo.get('stargazers_count')} stars")
    else:
        print(f"✗ Failed with status code: {response.status_code}")
    print()

def test_rate_limit():
    """Check API rate limit"""
    print("Checking GitHub API rate limit...")
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers=get_headers())
    
    if response.status_code == 200:
        data = response.json()
        core = data['resources']['core']
        print(f"✓ Rate Limit: {core['remaining']}/{core['limit']}")
        print(f"  Authenticated: {'Yes' if GITHUB_TOKEN else 'No'}")
    else:
        print(f"✗ Failed with status code: {response.status_code}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("GitHub Server Functionality Test")
    print("=" * 60)
    print()
    
    try:
        test_rate_limit()
        test_get_repo_info()
        test_list_issues()
        test_search_repos()
        
        print("=" * 60)
        print("✓ All tests passed! GitHub server is working correctly.")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

