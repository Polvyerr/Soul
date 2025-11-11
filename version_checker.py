import requests
import subprocess
import sys
import os

# Your GitHub repository details
GITHUB_USERNAME = "your-github-username"
REPO_NAME = "your-repo-name"
BRANCH = "main"  # or "master"

def get_current_commit():
    """Get the current local git commit hash"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except:
        return None

def get_latest_github_commit():
    """Get the latest commit hash from GitHub"""
    try:
        url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/commits/{BRANCH}"
        response = requests.get(url)
        if response.status_code == 200:
            commit_data = response.json()
            return commit_data['sha'][:7]  # Short commit hash
        return None
    except:
        return None

def check_for_updates():
    """Check if update is needed and notify user"""
    current = get_current_commit()
    latest = get_latest_github_commit()
    
    if not current or not latest:
        print("Could not check for updates. Continuing...")
        return False
    
    print(f"Your version: {current}")
    print(f"Latest version: {latest}")
    
    if current != latest:
        print("\n🚨 UPDATE REQUIRED!")
        print(f"Please update before using this script!")
        print(f"Run: git pull origin {BRANCH}")
        print(f"Or download from: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
        return True
    
    print("✅ You have the latest version!")
    return False

if __name__ == "__main__":
    if check_for_updates():
        sys.exit(1)  # Exit with error code to block usage