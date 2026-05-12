import json
from config import STATE_FILE


def load() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def get_last_sha() -> str:
    return load().get("last_processed_sha", "")


def set_last_sha(sha: str) -> None:
    state = load()
    state["last_processed_sha"] = sha
    save(state)
