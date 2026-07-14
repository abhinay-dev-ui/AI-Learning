"""
employee.py

Demonstrates

✔ Importing another module

✔ Shared module state

✔ __name__
"""

print("Loading Employee Module")

import config

print(f"Current Counter = {config.counter}")

config.counter += 5

print(f"Counter Updated = {config.counter}")

print(f"__name__ = {__name__}")


def create_employee():

    print("Employee Created")


if __name__ == "__main__":

    print("employee.py executed directly")

else:

    print("employee.py imported")