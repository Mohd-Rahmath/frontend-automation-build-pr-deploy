# frontend-automation-build-pr-deploy

A Python CLI that watches the `dev` branch of **aplx-react-project-genie**, runs `npm run build`, and automatically opens a GitHub PR to `main` — powered by LangChain and Claude (Anthropic).

## How it works

```
New commit on dev branch
        ↓
  git pull origin dev  (local project)
        ↓
  npm run build
        ↓  (build passes)
  Create PR: dev → main  (GitHub API)
        ↓
  Save last-processed SHA  (.state.json)
```

The LangChain ReAct agent drives each step and uses Claude to write professional PR descriptions from your commit history.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
copy .env.example .env
```

Edit `.env` and fill in:

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | From https://console.anthropic.com |
| `GITHUB_TOKEN` | GitHub PAT with `repo` + `pull_requests` scopes |
| `GITHUB_REPO` | `ApplexusLabsPrivate/aplx-react-project-genie` |
| `DEV_BRANCH` | `dev` (default) |
| `MAIN_BRANCH` | `main` (default) |
| `PROJECT_PATH` | Local path to the React project |
| `POLL_INTERVAL` | Seconds between checks in watch mode (default `60`) |

## Usage

### Run once
```bash
python main.py run
```
Checks for new commits → pulls → builds → creates PR (if build passes).

### Watch mode (continuous polling)
```bash
python main.py watch
# or override poll interval:
python main.py watch --interval 120
```

### Show current config & state
```bash
python main.py status
```

## Project structure

```
frontend-automation-build-pr-deploy/
├── main.py          # Click CLI (run / watch / status)
├── agent.py         # LangChain ReAct agent + prompt
├── tools.py         # LangChain tools (git, build, GitHub API)
├── config.py        # Env var loader
├── requirements.txt
└── .env.example
```

## Requirements

- Python 3.11+
- Node.js / npm (for the build step)
- Git installed and the React project already cloned locally
- GitHub PAT with write access to the repo
