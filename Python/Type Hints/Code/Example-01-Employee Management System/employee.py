from typing import Final, ClassVar, Literal, TypeAlias, NewType

# -----------------------------
# Type Aliases
# -----------------------------

EmployeeId = NewType("EmployeeId", int)
Department = Literal["Engineering", "HR", "Finance", "Sales"]

Salary = float

SearchValue: TypeAlias = int | str


class Employee:

    COMPANY: ClassVar[str] = "OpenAI Technologies"

    DEFAULT_BONUS: Final[float] = 5000.0

    def __init__(
        self,
        employee_id: EmployeeId,
        name: str,
        department: Department,
        salary: Salary,
    ) -> None:

        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.salary = salary

    def display(self) -> None:
        print(
            f"{self.employee_id} | "
            f"{self.name} | "
            f"{self.department} | "
            f"{self.salary}"
        )