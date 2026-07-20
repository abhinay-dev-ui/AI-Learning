"""
Employee Service

Contains business logic for employee-related operations.

Author: GenAI Learning Roadmap
"""

from database.connection import DatabaseConnection
from models.employee import Employee


class EmployeeService:
    """Handles employee business operations."""

    def register_employee(
        self,
        db: DatabaseConnection,
        employee: Employee,
        simulate_failure: bool = False,
    ) -> None:
        """
        Register a new employee.

        Args:
            db: Active database connection.
            employee: Employee to register.
            simulate_failure: Raises an exception to demonstrate rollback.
        """

        self._save_employee(db, employee)
        self._create_payroll(db, employee)

        if simulate_failure:
            raise RuntimeError("Payroll service is unavailable.")

        self._create_audit_log(db, employee)

    def _save_employee(
        self,
        db: DatabaseConnection,
        employee: Employee,
    ) -> None:
        """Persist employee information."""

        db.execute(
            f"""
            INSERT INTO employees (id, name, department)
            VALUES ({employee.employee_id},
                    '{employee.name}',
                    '{employee.department}')
            """
        )

    def _create_payroll(
        self,
        db: DatabaseConnection,
        employee: Employee,
    ) -> None:
        """Create payroll record."""

        db.execute(
            f"""
            INSERT INTO payroll (employee_id)
            VALUES ({employee.employee_id})
            """
        )

    def _create_audit_log(
        self,
        db: DatabaseConnection,
        employee: Employee,
    ) -> None:
        """Create audit entry."""

        db.execute(
            f"""
            INSERT INTO audit_log (message)
            VALUES ('Employee {employee.employee_id} registered.')
            """
        )