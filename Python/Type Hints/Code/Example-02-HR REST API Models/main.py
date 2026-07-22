from employee_api import (
    create_employee,
    get_employee,
    list_employees,
)

from models import EmployeeRequest


def main() -> None:

    request: EmployeeRequest = {
        "name": "John",
        "department": "Engineering",
        "salary": 85000,
    }

    response = create_employee(request)

    print("Employee Created")

    print(response)

    print("\nEmployee Details")

    employee = get_employee(101)

    print(employee)

    print("\nEmployee Summary")

    for employee in list_employees():

        print(employee)


if __name__ == "__main__":
    main()