memory_store = []

def store_event(event):
    memory_store.append(event)

def get_memory():
    return memory_store[-5:]