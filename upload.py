import os
import base64
import requests

# --- CONFIGURATION ---
GITHUB_TOKEN = "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"  # Put your token here
GITHUB_REPO = "https://github.com/Avinaykumar26/Medical-Abbreviation-Expander.git"  # e.g., "tarun/medical-expander"
BRANCH = "main"

# Files/folders to ignore (like .gitignore)
IGNORE_LIST = [".venv", "__pycache__", ".git", "upload.py", ".streamlit"]

def upload_file(file_path, repo_path):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{repo_path}"
    
    # Get current file if it exists (for the SHA)
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    sha = r.json().get("sha") if r.status_code == 200 else None

    with open(file_path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf-8")

    data = {
        "message": f"Upload {repo_path}",
        "content": content,
        "branch": BRANCH
    }
    if sha:
        data["sha"] = sha

    r = requests.put(url, json=data, headers=headers)
    if r.status_code in [200, 201]:
        print(f"✅ Uploaded: {repo_path}")
    else:
        print(f"❌ Failed {repo_path}: {r.json()}")

def main():
    if GITHUB_TOKEN == "YOUR_TOKEN_HERE":
        print("Error: Please set your GITHUB_TOKEN in the script first!")
        return

    for root, dirs, files in os.walk("."):
        # filter ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_LIST]
        
        for file in files:
            if any(ignore in os.path.join(root, file) for ignore in IGNORE_LIST):
                continue
                
            local_path = os.path.join(root, file)
            # Convert backslashes for GitHub
            repo_path = local_path.replace(".\\", "").replace("\\", "/")
            upload_file(local_path, repo_path)

if __name__ == "__main__":
    main()
