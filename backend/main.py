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
@app.get("/machines")
def get_machines():
    cursor.execute("SELECT name, heat FROM machines")
    rows = cursor.fetchall()

    return [{"name": r[0], "heat": r[1]} for r in rows]
@app.post("/spin")
async def log_spin(data: dict):
    name = data["machine"]
    win = data["win"]
    bonus = data["bonus"]

    # ensure machine exists
    cursor.execute("INSERT OR IGNORE INTO machines (name) VALUES (?)", (name,))

    cursor.execute("""
        SELECT spins_since_bonus, total_spins, total_wins
        FROM machines WHERE name=?
    """, (name,))
    row = cursor.fetchone()

    spins_since_bonus, total_spins, total_wins = row

    total_spins += 1

    if bonus:
        spins_since_bonus = 0
    else:
        spins_since_bonus += 1

    if win > 0:
        total_wins += 1

    # 🔥 smarter heat formula
    avg_cycle = 80  # assumed average
    cycle_score = min(100, (spins_since_bonus / avg_cycle) * 100)
    win_rate = (total_wins / total_spins) * 100

    heat = int((cycle_score * 0.7) + (win_rate * 0.3))

    cursor.execute("""
        UPDATE machines
        SET heat=?, spins_since_bonus=?, total_spins=?, total_wins=?
        WHERE name=?
    """, (heat, spins_since_bonus, total_spins, total_wins, name))

    cursor.execute("""
        INSERT INTO spins (machine, win, bonus)
        VALUES (?, ?, ?)
    """, (name, win, bonus))

    conn.commit()

    await broadcast()

    return {"heat": heat}
@app.get("/recent-wins")
def recent_wins():
    cursor.execute("""
        SELECT machine, win, created_at
        FROM spins
        WHERE win > 0
        ORDER BY created_at DESC
        LIMIT 10
    """)
    rows = cursor.fetchall()

    return [
        {"machine": r[0], "win": r[1], "time": r[2]}
        for r in rows
    ]
const [wins, setWins] = useState([]);
useEffect(() => {
  fetch(API + "/recent-wins")
    .then(res => res.json())
    .then(setWins);
}, []);
<h2>💰 Recent Wins</h2>

{wins.map((w, i) => (
  <div key={i}>
    ${w.win} – {w.machine}
  </div>
))}
