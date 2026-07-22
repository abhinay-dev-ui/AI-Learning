from typing import Annotated

EmployeeName = Annotated[
    str,
    "Employee name must not be empty",
]

Salary = Annotated[
    float,
    "Salary must be greater than zero",
]