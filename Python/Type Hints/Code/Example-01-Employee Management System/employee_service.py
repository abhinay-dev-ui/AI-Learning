from employee import Employee, EmployeeId, SearchValue

class EmployeeService:

    def __init__(self) -> None:
        self._employees: list[Employee] = []

    def add_employee(self, employee: Employee) -> None:
        self._employees.append(employee)

    def get_employee(self, employee_id: EmployeeId) -> Employee | None:

        for employee in self._employees:
            if employee.employee_id == employee_id:
                return employee

        return None

    def search(self, value: SearchValue) -> list[Employee]:

        result: list[Employee] = []

        for employee in self._employees:

            if (
                employee.employee_id == value
                or employee.name == value
            ):
                result.append(employee)

        return result

    def display_all(self) -> None:

        for employee in self._employees:
            employee.display()