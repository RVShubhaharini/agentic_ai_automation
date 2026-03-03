from fastapi import FastAPI
from scheduler import start_scheduler
from memory import get_memory

app = FastAPI()

# Start scheduler immediately when app loads
start_scheduler()
print("Scheduler started")

# IMPORTANT: Allow GET + HEAD for UptimeRobot
@app.api_route("/", methods=["GET", "HEAD"])
def home():
    return {"status": "Agentic AI Running"}

@app.get("/memory")
def memory():
    return {"recent_events": get_memory()}