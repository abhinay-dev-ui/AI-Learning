from database.connection import connect

def generate_embedding():
    connect()
    print("Embedding Generated")