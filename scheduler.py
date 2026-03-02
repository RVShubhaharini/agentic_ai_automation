from apscheduler.schedulers.background import BackgroundScheduler
from agents import monitoring_agent, analysis_agent, prediction_agent
from decision_engine import decision_agent
from actions import action_agent
from alerts import send_weather_alert

def run_agents():
    event = monitoring_agent()
    analysis = analysis_agent(event)
    prediction = prediction_agent(event)
    decision = decision_agent(analysis, prediction)
    action = action_agent(decision)

    send_weather_alert(event, analysis, prediction)

    print("Agent Cycle Complete:", action)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_agents, 'interval', minutes=5)
    scheduler.start()