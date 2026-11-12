"""
GitHub App identity: push and open PRs as the app bot.

Reads GH_APP_ID from the environment and the private key from /run/secrets, so no secret
appears in commands or output.

    githubPrs.py check <repo>
    githubPrs.py push <repo> <clonePath> <branch>
    githubPrs.py pr <repo> <branch> <title> <bodyFile> [base]
"""
import base64
import glob
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

import jwt  # *** PyJWT, supplied by `uv run --with 'pyjwt[crypto]'`

ORGANIZATION = "PETROGEO-UFRN"


def api(method: str, path: str, token: str, body=None):
    request = urllib.request.Request(
        f"https://api.github.com{path}",
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, json.loads(response.read() or b"{}")
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read() or b"{}")


def readPrivateKey() -> str:
    keyPaths = glob.glob("/run/secrets/*.private-key.pem")
    if not keyPaths:
        raise SystemExit("no /run/secrets/*.private-key.pem")
    # *** a compose file mount whose host source is missing shows up as an empty directory
    if not os.path.isfile(keyPaths[0]):
        raise SystemExit(f"{keyPaths[0]} is not a file: its compose mount source is missing on the host")
    return open(keyPaths[0]).read()


def appToken(repoName: str) -> tuple[str, dict]:
    """One-hour installation token scoped to a single repo, and the permissions it grants."""
    if not os.environ.get("GH_APP_ID"):
        raise SystemExit("GH_APP_ID is not set")

    now = int(time.time())
    appJwt = jwt.encode(
        {"iat": now - 60, "exp": now + 540, "iss": os.environ["GH_APP_ID"]},
        readPrivateKey(),
        algorithm="RS256",
    )
    status, installation = api("GET", f"/repos/{ORGANIZATION}/{repoName}/installation", appJwt)
    if status != 200:
        raise SystemExit(f"app not installed on {repoName}: {status}")
    status, token = api(
        "POST", f"/app/installations/{installation['id']}/access_tokens", appJwt,
        {"repositories": [repoName]},
    )
    if status != 201:
        raise SystemExit(f"token mint failed: {status}")
    return token["token"], token["permissions"]


def check(repoName: str) -> None:
    _, permissions = appToken(repoName)
    for name in ("contents", "pull_requests", "workflows"):
        print(name, permissions.get(name, "none"))


def push(repoName: str, clonePath: str, branch: str) -> None:
    token, _ = appToken(repoName)
    credentials = base64.b64encode(f"x-access-token:{token}".encode()).decode()
    # *** passed per command, so the token never lands in .git/config
    result = subprocess.run(
        ["git", "-c", f"http.extraHeader=Authorization: Basic {credentials}",
         "push", "-q", "origin", f"{branch}:{branch}"],
        cwd=clonePath, capture_output=True, text=True,
    )
    print((result.stdout + result.stderr).replace(token, "***").replace(credentials, "***"))
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def openPullRequest(repoName: str, branch: str, title: str, bodyFile: str, base: str = "main") -> None:
    token, _ = appToken(repoName)
    status, pullRequest = api(
        "POST", f"/repos/{ORGANIZATION}/{repoName}/pulls", token,
        {"title": title, "head": branch, "base": base, "body": open(bodyFile).read()},
    )
    if status != 201:
        raise SystemExit(f"PR failed: {status} {pullRequest.get('message')}")
    print(pullRequest["html_url"], pullRequest["user"]["login"])


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "check" and len(sys.argv) == 3:
        check(sys.argv[2])
        raise SystemExit(0)
    if command == "push" and len(sys.argv) == 5:
        push(*sys.argv[2:5])
        raise SystemExit(0)
    if command == "pr" and len(sys.argv) in (6, 7):
        openPullRequest(*sys.argv[2:])
        raise SystemExit(0)
    raise SystemExit(__doc__)
