import json
import os
import subprocess
import sys

from config import PROJECT_PATH


def run_build() -> str:
    npm = "npm.cmd" if sys.platform == "win32" else "npm"
    env = {**os.environ, "CI": "false"}

    try:
        result = subprocess.run(
            [npm, "run", "build"],
            cwd=str(PROJECT_PATH),
            capture_output=True,
            text=True,
            timeout=300,
            env=env,
        )

        stdout = result.stdout[-4000:] if len(result.stdout) > 4000 else result.stdout
        stderr = result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr

        if result.returncode == 0:
            return json.dumps({"status": "success", "output": stdout})

        return json.dumps(
            {
                "status": "failed",
                "output": stdout,
                "error": stderr,
                "exit_code": result.returncode,
            }
        )
    except subprocess.TimeoutExpired:
        return json.dumps({"status": "timeout", "error": "Build timed out after 5 minutes"})
    except Exception as exc:
        return json.dumps({"status": "error", "error": str(exc)})
