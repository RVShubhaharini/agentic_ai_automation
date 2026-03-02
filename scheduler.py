from apscheduler.schedulers.background import BackgroundScheduler
from agents import monitoring_agent, analysis_agent, prediction_agent
from decision_engine import decision_agent
from actions import action_agent
from alerts import send_weather_alert

def run_agents():
    event = monitoring_agent()
    analysis = analysis_agent(event)
    prediction = prediction_agent(event)
    decisions = decision_agent(analysis, prediction)
    actions = action_agent(decisions)

    send_weather_alert(event, analysis, prediction, actions)

    print("Agent Cycle Complete:", actions)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_agents, 'interval', minutes=5)
    scheduler.start()