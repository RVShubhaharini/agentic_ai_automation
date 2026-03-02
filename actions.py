from memory import store_event

def action_agent(decision):
    
    if decision == "COOLING_REQUIRED":
        action = "Ventilation Activated"
        
    elif decision == "SEND_ALERT":
        action = "Heat Alert Sent"
        
    else:
        action = "No Action Needed"
        
    store_event({"action": action})
    return action