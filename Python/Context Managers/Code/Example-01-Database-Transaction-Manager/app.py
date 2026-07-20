"""
Application Entry Point

Demonstrates successful and failed transactions.

Author: GenAI Learning Roadmap
"""

from database.transaction_manager import TransactionManager
from models.employee import Employee
from services.employee_service import EmployeeService


def successful_transaction() -> None:
    """Demonstrates a successful transaction."""

    employee = Employee(
        employee_id=101,
        name="Alice",
        department="Engineering",
    )

    service = EmployeeService()

    with TransactionManager() as db:
        service.register_employee(db, employee)


def failed_transaction() -> None:
    """Demonstrates automatic rollback."""

    employee = Employee(
        employee_id=102,
        name="Bob",
        department="Finance",
    )

    service = EmployeeService()

    try:
        with TransactionManager() as db:
            service.register_employee(
                db,
                employee,
                simulate_failure=True,
            )

    except RuntimeError as error:
        print(f"\nApplication Error: {error}\n")


def main() -> None:

    print("\n========== Successful Transaction ==========\n")
    successful_transaction()

    print("\n========== Failed Transaction ==========\n")
    failed_transaction()


if __name__ == "__main__":
    main()