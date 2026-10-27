"""Create a private GitHub repository and upload this project's files via REST API.

Usage:
  GITHUB_TOKEN=... python deploy_to_github.py
Optional:
  GITHUB_OWNER=your-user-or-org
  GITHUB_REPO=autonomous-media-pipeline
  GITHUB_PRIVATE=true
"""
import base64
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN = os.environ.get("GITHUB_TOKEN")
REPO = os.environ.get("GITHUB_REPO", "autonomous-media-pipeline")
PRIVATE = os.environ.get("GITHUB_PRIVATE", "true").lower() != "false"

if not TOKEN:
    raise SystemExit("Set GITHUB_TOKEN with repo creation/write permissions.")
API = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "autonomous-media-pipeline-deployer",
    "Content-Type": "application/json",
}


def request(method, path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(API + path, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        if exc.code == 404:
            return None
        raise RuntimeError(f"GitHub API {exc.code}: {detail}") from exc


user = request("GET", "/user")
owner = os.environ.get("GITHUB_OWNER", user["login"])
if owner == user["login"]:
    repo = request("GET", f"/repos/{owner}/{REPO}")
    if repo is None:
        repo = request("POST", "/user/repos", {
            "name": REPO, "private": PRIVATE,
            "description": "Automated pipeline for processing and archiving authorized media.",
            "auto_init": True,
        })
else:
    repo = request("GET", f"/repos/{owner}/{REPO}")
    if repo is None:
        repo = request("POST", f"/orgs/{owner}/repos", {
            "name": REPO, "private": PRIVATE,
            "description": "Automated pipeline for processing and archiving authorized media.",
            "auto_init": True,
        })

branch = repo.get("default_branch") or "main"
try:
    ref = request("GET", f"/repos/{owner}/{REPO}/git/ref/heads/{branch}")
    base_sha = ref["object"]["sha"]
except Exception:
    base_sha = None

files = []
for path in sorted(ROOT.rglob("*")):
    if not path.is_file() or ".git" in path.parts or path.name == "__pycache__":
        continue
    rel = path.relative_to(ROOT).as_posix()
    content = path.read_bytes()
    blob = request("POST", f"/repos/{owner}/{REPO}/git/blobs", {
        "content": base64.b64encode(content).decode(),
        "encoding": "base64",
    })
    files.append({"path": rel, "mode": "100644", "type": "blob", "sha": blob["sha"]})

tree_payload = {"tree": files}
if base_sha:
    parent_commit = request("GET", f"/repos/{owner}/{REPO}/git/commits/{base_sha}")
    tree_payload["base_tree"] = parent_commit["tree"]["sha"]
tree = request("POST", f"/repos/{owner}/{REPO}/git/trees", tree_payload)
commit_payload = {
    "message": "Add licensed media processing pipeline",
    "tree": tree["sha"],
}
if base_sha:
    commit_payload["parents"] = [base_sha]
commit = request("POST", f"/repos/{owner}/{REPO}/git/commits", commit_payload)
if base_sha:
    request("PATCH", f"/repos/{owner}/{REPO}/git/refs/heads/{branch}", {
        "sha": commit["sha"], "force": False,
    })
else:
    request("POST", f"/repos/{owner}/{REPO}/git/refs", {
        "ref": f"refs/heads/{branch}", "sha": commit["sha"],
    })
print(f"Repository: https://github.com/{owner}/{REPO}")
print(f"Commit: {commit['sha']}")
print("Configure repository Actions secrets before enabling the scheduled workflow.")
