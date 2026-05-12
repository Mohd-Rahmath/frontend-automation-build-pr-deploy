from fastapi import APIRouter
from services import main_service

router = APIRouter(prefix="/main", tags=["Main"])


@router.post("/pull-build")
def pull_and_build():
    """Pull main branch and run npm run build."""
    pull_result = main_service.pull()

    if "failed" in pull_result or "error" in pull_result:
        return {"status": "failed", "step": "pull", "detail": pull_result}

    build_result = main_service.build()

    return {
        "branch": main_service.BRANCH,
        "pull": pull_result,
        "build": build_result["status"],
        "detail": build_result.get("output") or build_result.get("error", ""),
    }
