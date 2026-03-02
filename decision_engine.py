def decision_agent(analysis, prediction):
    
    if analysis['risk'] == "HIGH_HEAT":
        return "COOLING_REQUIRED"
    
    if prediction['prediction'] == "HEAT_STRESS_RISK":
        return "SEND_ALERT"
    
    return "NO_ACTION"