from typing import TypedDict, NamedTuple, Literal

# -----------------------------
# Request Models
# -----------------------------

Department = Literal["Engineering", "HR", "Finance", "Sales"]


class EmployeeRequest(TypedDict):
    name: str
    department: Department
    salary: float


class EmployeeResponse(TypedDict):
    employee_id: int
    name: str
    department: Department
    salary: float
    status: Literal["Created", "Success"]


# -----------------------------
# Lightweight Read Model
# -----------------------------


class EmployeeSummary(NamedTuple):
    employee_id: int
    name: str