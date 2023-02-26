from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"msg": "The app is functioning!"}


@app.get("/ping")
async def ping():
    return {"ping": "some amount of time"}
