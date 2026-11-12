# Agent container (boto-dev-agent)

A Hermes agent (Claude) in a rootless, capability-free container, for developing
botoseis-web: the Flask API, the Bokeh visualization services and the React clients.
Start it with `make agent`.

The image (`agent/dockerfile`) is built on the same Seismic Unix image as the server
(44R28, `CWPROOT=/opt/cwp/44R28`, pinned by digest), with Python 3.12, uv, Node 22.18
(the clients' version) and yarn/pnpm through corepack.

## What it can change

| Path | Access | Why |
| --- | --- | --- |
| repo root (`server/`, `workspace/`, `admin/`, `docs/`, new folders, ...) | read-write | the work itself |
| `.git` | read-only | it is the host's checkout; the agent opens PRs from its own clone in its Hermes volume |
| `.github/`, `LICENSE`, `.gitignore` | read-only | CI workflows and repo policy |
| `Makefile`, `docker-compose.yml`, `agent/`, `.agents/` | read-only | its own container and config |
| `.agents/hermes.yaml` | read-write | mounted as its Hermes config, so `hermes config set` works |
| `.secrets/` | hidden | credentials, only the GitHub App key is mounted read-only at `/run/secrets` |
| `.env` files (root and per service), `*.pem`, `*.key` | hidden | each one that exists is covered by an empty read-only file |

The hidden files are listed by `agent/secret-masks.sh` when `make agent` runs, into the
gitignored `.secrets/agent-masks.yml` compose override. A secret file added later stays
visible until the next `make agent`, which recreates the container with its mask.

Python virtualenvs go in `~/.venvs` (the `agent-venv` volume), never in the repo, e.g.
`uv venv ~/.venvs/server --python 3.12 && uv pip install --python ~/.venvs/server -r server/requirements.txt -r server/requirements-dev.txt`.

## Setup

1. Optional, for pushes and PRs: GitHub App credentials in `.secrets/` (gitignored,
   hidden inside the container):
   - `agent.env` with `GH_APP_ID=<GitHub App id>`;
   - the GitHub App private key (`*.private-key.pem`), mounted read-only at `/run/secrets`.

   Without them the agent still starts and works on the code; `make agent` just warns
   that it cannot push or open PRs.
2. `make agent` (always through it: it hides the secret files and sets the engine's
   options). On the first start, log in to Claude: `claude` -> `/login`, then
   `hermes chat --provider anthropic`. Detach without stopping it with `ctrl + P + Q`.

The agent's repo skills live in `.agents/skills/` (`github-prs`: pushes and PRs as the
GitHub App).

The service is in the `agent` compose profile, so `docker compose up`/`build` and the
other make targets leave it out. It works with docker or rootless podman (podman-compose
>= 1.1); the Makefile picks podman when installed.

## Server tests

The agent cannot start containers. Run `make test` on the host to bring up `db-test` and
apply the migrations; the agent reaches it by service name (`DATABASE_HOST=db-test`,
`TEST_DATABASE_PORT=5432` are set in its environment) and runs `cd server && pytest`.
