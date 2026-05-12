import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "ApplexusLabsPrivate/aplx-react-project-genie")
DEV_BRANCH = os.getenv("DEV_BRANCH", "Dev-v1")
MAIN_BRANCH = os.getenv("MAIN_BRANCH", "Test-v1")
PROJECT_PATH = Path(
    os.getenv(
        "PROJECT_PATH",
        r"C:\Users\mrali\Documents\applications\consenz-frontend-deployment\aplx-react-project-genie",
    )
)
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "60"))
LLM_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-4-6")

STATE_FILE = Path(__file__).parent / ".state.json"
GITHUB_API_BASE = "https://api.github.com"
DEPLOY_PATH = Path(os.getenv("DEPLOY_PATH", r"C:\Users\mrali\Documents"))
