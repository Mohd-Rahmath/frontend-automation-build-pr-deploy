from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from config import DEPLOY_PATH
from services import copy_build_service

router = APIRouter(prefix="/copy-build", tags=["Copy Build"])


class CopyRequest(BaseModel):
    destination: str = str(DEPLOY_PATH)


@router.post("/")
def copy_build(body: CopyRequest = CopyRequest()):
    """Copy the dist/ build folder to the given destination path."""
    result = copy_build_service.copy_build(Path(body.destination))
    return result
