from fastapi import FastAPI
from loguru import logger as log

from api.database import database
from api.database.models import LinkMap

app = FastAPI()


@app.on_event("startup")
async def startup_event() -> None:
    log.info("Connecting to the database...")

    await database.connect()

    log.info("Connected to the database.")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await database.disconnect()

    log.info("Disconnected from database.")


@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"ping": "some amount of time"}


@app.post("/link_map", response_model=LinkMap)
async def create_link_map(link_map: LinkMap) -> LinkMap:
    return await link_map.save()


@app.get("/link_map", response_model=list[LinkMap])
async def get_user_specific_link_maps(sid: int, uid: int) -> list[LinkMap]:
    return await LinkMap.objects.all(sid=sid, uid=uid)
