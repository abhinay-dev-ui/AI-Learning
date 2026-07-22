from employee import Employee
from employee import EmployeeId
from employee_service import EmployeeService


def main() -> None:

    service = EmployeeService()

    service.add_employee(
        Employee(
            EmployeeId(101),
            "John",
            "Engineering",
            85000,
        )
    )

    service.add_employee(
        Employee(
            EmployeeId(102),
            "Alice",
            "HR",
            65000,
        )
    )

    print("----- All Employees -----")

    service.display_all()

    print("\nSearching by ID")

    employee = service.get_employee(EmployeeId(101))

    if employee:
        employee.display()

    print("\nSearching by Name")

    employees = service.search("Alice")

    for employee in employees:
        employee.display()


if __name__ == "__main__":
    main()