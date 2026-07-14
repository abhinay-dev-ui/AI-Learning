"""
====================================================
Example 1 : Python Modules - Core Concepts
====================================================

Concepts Covered

1. Creating modules
2. Importing modules
3. Module caching
4. __name__
5. __main__
6. Top-level execution
7. Shared module state
8. sys.modules

Run:
python main.py

Expected Learning

Observe that:

✔ config.py executes only once.
✔ employee.py executes only once.
✔ Multiple imports reuse cached modules.
✔ Module state is shared.
"""

import sys

print("=" * 50)
print("Main Program Started")
print("=" * 50)

import config

print()

import employee

print()

print("Importing config again...")

import config

print()

print(f"Counter : {config.counter}")

config.counter += 1

print(f"Counter after update : {config.counter}")

print()

print("Is config cached?")

print("config" in sys.modules)

print()

print("Main Program Finished")