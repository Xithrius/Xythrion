from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    return {"msg": "The app is functioning!"}

@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"ping": "some amount of time"}
