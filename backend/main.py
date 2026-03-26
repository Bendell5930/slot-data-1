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
@app.get("/machine-list")
def machine_list():
    cursor.execute("SELECT name FROM machines ORDER BY name ASC")
    rows = cursor.fetchall()

    return [r[0] for r in rows]
    machines = [
    "Dragon Link #24",
    "Lightning Link #11",
    "Buffalo Gold #6"
]

for m in machines:
    cursor.execute("INSERT OR IGNORE INTO machines (name) VALUES (?)", (m,))

conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS casinos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS machines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    casino_id INTEGER,
    heat INTEGER DEFAULT 50,
    spins_since_bonus INTEGER DEFAULT 0,
    total_spins INTEGER DEFAULT 0,
    total_wins INTEGER DEFAULT 0,
    UNIQUE(name, casino_id)
)
""")
casinos = ["Star Brisbane", "Treasury Casino"]

for c in casinos:
    cursor.execute("INSERT OR IGNORE INTO casinos (name) VALUES (?)", (c,))

# Example machines
cursor.execute("SELECT id FROM casinos WHERE name='Star Brisbane'")
star_id = cursor.fetchone()[0]

machines = [
    ("Dragon Link #24", star_id),
    ("Lightning Link #11", star_id)
]

for m in machines:
    cursor.execute("INSERT OR IGNORE INTO machines (name, casino_id) VALUES (?, ?)", m)

conn.commit()
@app.get("/casinos")
def get_casinos():
    cursor.execute("SELECT id, name FROM casinos")
    return [{"id": r[0], "name": r[1]} for r in cursor.fetchall()]
    @app.get("/machines/{casino_id}")
def get_machines(casino_id: int):
    cursor.execute("""
        SELECT name, heat FROM machines WHERE casino_id=?
    """, (casino_id,))
    return [{"name": r[0], "heat": r[1]} for r in cursor.fetchall()]
    cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")
    @app.post("/register")
def register(data: dict):
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (data["username"], data["password"])
        )
        conn.commit()
        return {"status": "ok"}
    except:
        return {"error": "User exists"}
        @app.post("/login")
def login(data: dict):
    cursor.execute(
        "SELECT id FROM users WHERE username=? AND password=?",
        (data["username"], data["password"])
    )
    user = cursor.fetchone()

    if user:
        return {"status": "ok", "user_id": user[0]}
    return {"error": "Invalid login"}
    if win > 50:  # threshold for alert
    alert = {
        "type": "big_win",
        session = stripe.checkout.Session.create(
    ...
    metadata={
        "user_id": user_id
    }
)
        "machine": name,
        "amount": win
    }

    for conn in connections:
        await conn.send_json(alert)
user_id = session["metadata"]["user_id"]
user_id = session["metadata"]["user_id"]
cursor.execute("""
ALTER TABLE users ADD COLUMN trial_end TIMESTAMP
""")
if event["type"] == "checkout.session.completed":
    session = event["data"]["object"]
    user_id = session["metadata"]["user_id"]

    subscription = stripe.Subscription.retrieve(
        session["subscription"]
    )

    trial_end = subscription["trial_end"]

    cursor.execute("""
        UPDATE users
        SET is_premium=1, trial_end=?
        WHERE id=?
    """, (trial_end, user_id))

    conn.commit()
session = stripe.checkout.Session.create(
    ...
    metadata={
        "user_id": user_id
    }
)
user_id = session["metadata"]["user_id"]
@app.post("/create-checkout-session")
def create_checkout(user_id: int):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{
            "price": "YOUR_PRICE_ID",
            "quantity": 1,
        }],
        subscription_data={
            "trial_period_days": 7
        },
        metadata={
            "user_id": user_id
        },
        success_url="https://your-frontend-url/success",
        cancel_url="https://your-frontend-url/cancel",
    )

    return {"url": session.url}
    cursor.execute("""
ALTER TABLE users ADD COLUMN trial_end TIMESTAMP
""")
    if event["type"] == "checkout.session.completed":
    session = event["data"]["object"]
    user_id = session["metadata"]["user_id"]

    subscription = stripe.Subscription.retrieve(
        session["subscription"]
    )

    trial_end = subscription["trial_end"]

    cursor.execute("""
        UPDATE users
        pip install pyfcm
        from pyfcm import FCMNotification

push_service = FCMNotification(api_key="YOUR_FIREBASE_KEY")

def send_notification(title, body):
    push_service.notify_all_devices(
        message_title=title,
        message_body=body
    )
    if win > 50:
    send_notification(
        "💰 Big Win!",
        f"{name} just hit ${win}"
    )
    @app.get("/leaderboard")
def leaderboard():
    cursor.execute("""
        SELECT machine, SUM(win) as total
        FROM spins
        GROUP BY machine
        ORDER BY total DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    return [
        {"machine": r[0], "total": r[1]}
        for r in rows
    ]
    cursor.execute("""
CREATE TABLE IF NOT EXISTS user_spins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    machine TEXT,
    win REAL,
    bonus BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
user_id = data.get("user_id")

if user_id:
    cursor.execute("""
        INSERT INTO user_spins (user_id, machine, win, bonus)
        VALUES (?, ?, ?, ?)
    """, (user_id, name, win, bonus))
    @app.get("/user-stats/{user_id}")
def user_stats(user_id: int):
    cursor.execute("""
        SELECT COUNT(*), SUM(win)
        FROM user_spins
        WHERE user_id=?
    """, (user_id,))
    
    total_spins, total_wins = cursor.fetchone()

    return {
        "spins": total_spins or 0,
        "winnings": total_wins or 0
    }
    
        SET is_premium=1, trial_end=?
        WHERE id=?
    """, (trial_end, user_id))

    conn.commit()
    pip install python-jose passlib[bcrypt]
    from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    from auth import hash_password, verify_password, create_token
    @app.post("/register")
def register(data: dict):
    hashed = hash_password(data["password"])

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (data["username"], hashed)
    )
    conn.commit()

    return {"status": "ok"}
    @app.post("/login")
def login(data: dict):
    cursor.execute(
        "SELECT id, password FROM users WHERE username=?",
        (data["username"],)
    )
    user = cursor.fetchone()

    if user and verify_password(data["password"], user[1]):
        token = create_token({"user_id": user[0]})
        return {"token": token}

    return {"error": "Invalid login"}
    from fastapi import Depends
from fastapi.security import HTTPBearer
from jose import jwt

security = HTTPBearer()

def get_current_user(token=Depends(security)):
    payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    return payload["user_id"]
    @app.get("/user-stats")
def user_stats(user_id: int = Depends(get_current_user)):
@app.get("/admin/stats")
def admin_stats():
    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM spins")
    spins = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(win) FROM spins")
    revenue = cursor.fetchone()[0] or 0

    return {
        "users": users,
        "spins": spins,
        "total_wins": revenue
    }
pip install python-jose passlib[bcrypt]
    from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    from auth import hash_password, verify_password, create_token
    @app.post("/register")
def register(data: dict):
    hashed = hash_password(data["password"])

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (data["username"], hashed)
    )
    conn.commit()

    return {"status": "ok"}
    @app.post("/login")
def login(data: dict):
    cursor.execute(
        "SELECT id, password FROM users WHERE username=?",
        (data["username"],)
    )
    user = cursor.fetchone()

    if user and verify_password(data["password"], user[1]):
        token = create_token({"user_id": user[0]})
        return {"token": token}

    return {"error": "Invalid login"}
    from fastapi import Depends
from fastapi.security import HTTPBearer
from jose import jwt

security = HTTPBearer()

def get_current_user(token=Depends(security)):
    payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    return payload["user_id"]
    @app.get("/user-stats")
def user_stats(user_id: int = Depends(get_current_user)):
    
