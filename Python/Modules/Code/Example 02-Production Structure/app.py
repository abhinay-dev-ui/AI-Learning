from services.embedding import generate_embedding
from services.llm import load_model

print("Application Started")

load_model()
generate_embedding()

print("Application Finished")