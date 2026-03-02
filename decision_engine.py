def decision_agent(analysis, prediction):
    
    decisions = []
    
    # Heat-related decisions
    if analysis['risk'] == "HIGH_HEAT":
        decisions.append("COOLING_REQUIRED")
    
    if prediction['prediction'] == "HEAT_STRESS_RISK":
        decisions.append("SEND_ALERT")
        
    # Irrigation-related decisions (checking if 'Farmers need not' or 'skip' is in the prediction text)
    if "Farmers need not" in prediction.get('rain_prediction', '') or "skip" in prediction.get('rain_prediction', ''):
        decisions.append("SKIP_IRRIGATION")
    else:
        decisions.append("IRRIGATION_NEEDED")
        
    if not decisions:
        decisions.append("NO_ACTION")
        
    return decisions