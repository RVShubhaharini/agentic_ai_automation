from apscheduler.schedulers.background import BackgroundScheduler
from agents import monitoring_agent, llm_reasoning_agent
from actions import action_agent
from alerts import send_weather_alert

def run_agents():
    # 1. Gather Data
    event = monitoring_agent()
    
    # 2. LLM Reasoning (The Brain)
    llm_response = llm_reasoning_agent(event)
    
    # 3. Execution
    decisions = llm_response.get("decisions", ["NO_ACTION"])
    actions = action_agent(decisions)

    # 4. Notify
    # The alert function originally expected (event, analysis, prediction, actions).
    # We pass the full llm_response as both analysis and prediction to keep alerts.py simple.
    send_weather_alert(event, llm_response, llm_response, actions)

    print("Agent Cycle Complete:", actions)

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Keeping the 5 minute interval as per original code, suitable for UptimeRobot pings
    scheduler.add_job(run_agents, 'interval', minutes=1)
    scheduler.start()