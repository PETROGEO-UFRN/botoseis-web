---
name: github-prs
description: Use for git pushes, PRs or GitHub API reads as the app bot.
---

# GitHub PRs as the app

The agent works through a GitHub App, so its commits and PRs show as `local-hermes[bot]`
and the user can review them. `GH_TOKEN`, when present, is the user's own token: never push,
open PRs or comment with it.

## Credentials

- `GH_APP_ID`: environment variable, from compose `env_file`.
- App private key: `/run/secrets/*.private-key.pem`, mounted read-only.
- The repo's secrets folder (gitignored, holding `agent.env` and the key) is covered inside
  the container by an empty tmpfs mask ("Permission denied" is expected): it holds nothing,
  never ask to make it readable.

## Check (names only, never print values)

```bash
tr '\0' '\n' < /proc/1/environ | cut -d= -f1 | grep GH_APP_ID
ls -l /run/secrets/
python .agents/skills/github-prs/scripts/githubPrs.py check <repo>   # via uv, see below
```

`check` mints a token and prints the permissions it grants; `contents` and
`pull_requests` must be `write` before claiming you can push or open PRs.

When something is missing:
- `GH_APP_ID` in PID 1 but not in the shell: Hermes filtered it from the terminal.
- Not in PID 1: compose never injected it. Read the whole delivery chain in one pass, citing
  `path:line`: the compose service (`env_file:`, volumes), the make target, the Dockerfile
  and its entrypoint. A host `.env` or shell export only feeds `${...}` interpolation.
- The `.pem` path is an empty directory: the compose mount's source file doesn't exist on
  the host (renamed key), so the engine created an empty directory in its place.
- The fix for the user to apply (compose files are read-only for the agent): `env_file:`
  pointing at the secrets folder's `agent.env`, and the whole folder mounted at
  `/run/secrets:ro`, which never depends on the key's file name. Never
  put credentials in a Dockerfile `ENV`/`ARG`: they get baked into image layers.

## Rules

- The host checkout's `/workspace/.git` is read-only: never commit there. For a PR, work in
  a separate clone under `~/.hermes/work/<repo>` (a persistent volume).
- Commit author: `git -c user.name=Claude -c user.email=noreply@anthropic.com commit ...`.
- Push, open PRs and read the API (PR state, reviews, Actions logs) with the app token.
- The user also pushes to the agent's branches: fetch first; if the branch moved, rebase
  your commits onto it. Never force-push.
- Changing `.github/workflows/*` needs the app's `workflows: write`. Check every `uses:`
  ref exists before pushing (`GET /repos/<owner>/<action>/git/ref/tags/<ref>`).

## Script

`scripts/githubPrs.py` mints a one-hour installation token per call; the token never
reaches the output or `.git/config`. Run it from the repo root with uv (install uv into
`~/.local/bin` if missing; `--no-project` keeps uv from creating a `.venv` or touching
`uv.lock`):

```bash
alias githubPrs="uv run -q --no-project --python 3.12 --with 'pyjwt[crypto]' \
  python .agents/skills/github-prs/scripts/githubPrs.py"
githubPrs check <repo>
githubPrs push <repo> <clonePath> <branch>
githubPrs pr <repo> <branch> <title> <bodyFile>
```

After opening a PR, confirm the printed author is `local-hermes[bot]` and that
`git ls-remote origin <branch>` equals `git rev-parse HEAD`.
