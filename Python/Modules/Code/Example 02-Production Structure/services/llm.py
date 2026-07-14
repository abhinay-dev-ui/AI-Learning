from database.connection import connect

def load_model():
    connect()
    print("LLM Loaded")