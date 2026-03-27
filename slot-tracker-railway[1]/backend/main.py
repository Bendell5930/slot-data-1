from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List

app = FastAPI()

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory message storage
messages: List[dict] = []

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

@app.post("/messages")
def post_message(username: str, message: str):
    msg_obj = {
        "username": username,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    messages.append(msg_obj)
    return {"status": "success"}

@app.get("/messages")
def get_messages():
    return sorted(messages, key=lambda x: x["timestamp"], reverse=True)[:50]
