from fastapi import FastAPI
from loguru import logger as log

from api.database import database

app = FastAPI()

@app.on_event("startup")
async def startup_event() -> None:
    log.info("Connectiong to the database...")

    await database.connect()

    log.info("Connected to the database.")

@app.on_event("shutdown")
async def shutdown_event() -> None:
    await database.disconnect()

    log.info("Disconnected from database.")

@app.get("/")
async def root() -> dict[str, str]:
    return {"msg": "The app is functioning!"}

@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"ping": "some amount of time"}
