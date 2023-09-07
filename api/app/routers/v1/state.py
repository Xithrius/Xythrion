import os
import signal

from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/")
async def shutdown() -> None:
    os.kill(os.getpid(), signal.SIGTERM)

    return Response(status_code=200, content="Server shutting down...")
