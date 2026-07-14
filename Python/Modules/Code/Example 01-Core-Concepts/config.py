"""
config.py

Concepts

✔ Top-level code
✔ Module caching
✔ Shared state

Notice that this print statement executes only ONCE,
even if config is imported multiple times.
"""

print("Loading Configuration...")

counter = 0

DATABASE_URL = "localhost"

API_KEY = "sample-key"

print("Configuration Loaded")

print(f"__name__ = {__name__}")


if __name__ == "__main__":

    print("Running config.py directly")

else:

    print("config.py imported as module")