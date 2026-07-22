from models import (
    EmployeeRequest,
    EmployeeResponse,
    EmployeeSummary,
)

_EMPLOYEES: list[EmployeeResponse] = []
_NEXT_ID = 101


def create_employee(
    request: EmployeeRequest,
) -> EmployeeResponse:

    global _NEXT_ID

    employee: EmployeeResponse = {
        "employee_id": _NEXT_ID,
        "name": request["name"],
        "department": request["department"],
        "salary": request["salary"],
        "status": "Created",
    }

    _EMPLOYEES.append(employee)

    _NEXT_ID += 1

    return employee


def get_employee(
    employee_id: int,
) -> EmployeeResponse | None:

    for employee in _EMPLOYEES:

        if employee["employee_id"] == employee_id:
            return employee

    return None


def list_employees() -> list[EmployeeSummary]:

    return [

        EmployeeSummary(
            employee["employee_id"],
            employee["name"],
        )

        for employee in _EMPLOYEES
    ]