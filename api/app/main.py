from fastapi import FastAPI
from loguru import logger as log

from app.database import database
from app.routers import v1

app = FastAPI()

app.include_router(v1)


@app.on_event("startup")
async def startup_event() -> None:
    log.info("Connecting to the database...")

    await database.connect()

    log.info("Connected to the database.")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await database.disconnect()

    log.info("Disconnected from database.")
