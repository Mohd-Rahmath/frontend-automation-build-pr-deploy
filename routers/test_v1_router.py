from fastapi import APIRouter
from services import test_v1_service

router = APIRouter(prefix="/test-v1", tags=["Test-v1"])


@router.post("/pull-build")
def pull_and_build():
    """Pull Test-v1 branch and run npm run build."""
    pull_result = test_v1_service.pull()

    if "failed" in pull_result or "error" in pull_result:
        return {"status": "failed", "step": "pull", "detail": pull_result}

    build_result = test_v1_service.build()

    return {
        "branch": test_v1_service.BRANCH,
        "pull": pull_result,
        "build": build_result["status"],
        "detail": build_result.get("output") or build_result.get("error", ""),
    }
