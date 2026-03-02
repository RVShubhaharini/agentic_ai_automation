from memory import store_event

def action_agent(decisions):
    # Now expects a list of decisions
    actions_taken = []
    
    for decision in decisions:
        action = "No Action Needed"
        
        if decision == "COOLING_REQUIRED":
            action = "Ventilation Activated"
        elif decision == "SEND_ALERT":
            action = "Heat Alert Sent"
        elif decision == "SKIP_IRRIGATION":
            action = "Irrigation system PAUSED (Rain predicted)"
        elif decision == "IRRIGATION_NEEDED":
            action = "Irrigation system ACTIVATED (Dry predicted)"
            
        if action != "No Action Needed":
            actions_taken.append(action)
            
    if not actions_taken:
        actions_taken.append("No Action Needed")
        
    store_event({"actions": actions_taken})
    return actions_taken