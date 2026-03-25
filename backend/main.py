from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/machines")
def machines():
    return [
        {"name":"Dragon Link #24","heat":80},
        {"name":"Lightning Link #11","heat":55},
        {"name":"Buffalo Gold #6","heat":20}
    ]
from fastapi import Body
import asyncio

@app.post("/spin")
async def log_spin(data: dict = Body(...)):
    machine_name = data["machine"]
    win = data["win"]
    bonus = data["bonus"]

    for m in machines:
        if m["name"] == machine_name:
            # simple heat logic
            if bonus:
                m["heat"] = 100
            elif win > 0:
                m["heat"] += 5
            else:
                m["heat"] -= 3

            m["heat"] = max(0, min(100, m["heat"]))

    await broadcast()

    return {"status": "ok"}
from db import conn, cursor
