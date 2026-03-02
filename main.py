from fastapi import FastAPI
from scheduler import start_scheduler
from memory import get_memory

app = FastAPI()

@app.on_event("startup")
def startup_event():
    start_scheduler()

@app.get("/")
def home():
    return {"status": "Agentic AI Running"}

@app.get("/memory")
def memory():
    return {"recent_events": get_memory()}