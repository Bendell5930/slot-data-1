from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Slot Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MACHINES = [
    {"name": "Dragon Link #24", "heat": 80},
    {"name": "Lightning Link #11", "heat": 55},
    {"name": "Buffalo Gold #6", "heat": 20},
]

RECENT_WINS = []


@app.get("/")
def root() -> dict:
    return {"message": "Backend running"}


@app.get("/machines")
def get_machines() -> list[dict]:
    return MACHINES


@app.get("/machine-list")
def get_machine_list() -> list[str]:
    return [machine["name"] for machine in MACHINES]


@app.get("/recent-wins")
def recent_wins() -> list[dict]:
    return RECENT_WINS[:10]


@app.post("/spin")
def log_spin(data: dict = Body(...)) -> dict:
    machine_name = data.get("machine", "").strip()
    win = float(data.get("win", 0))
    bonus = bool(data.get("bonus", False))

    if not machine_name:
        return {"error": "Machine name is required"}

    machine = next((m for m in MACHINES if m["name"] == machine_name), None)
    if machine is None:
        machine = {"name": machine_name, "heat": 50}
        MACHINES.append(machine)

    if bonus:
        machine["heat"] = 100
    elif win > 0:
        machine["heat"] = min(100, machine["heat"] + 5)
    else:
        machine["heat"] = max(0, machine["heat"] - 3)

    if win > 0:
        RECENT_WINS.insert(0, {"machine": machine_name, "win": win})
        del RECENT_WINS[10:]

    return {"status": "ok", "heat": machine["heat"]}
