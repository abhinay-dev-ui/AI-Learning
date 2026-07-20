"""
Employee Domain Model

Represents an employee in the HR system.

Author: GenAI Learning Roadmap
"""

from dataclasses import dataclass


@dataclass
class Employee:
    """Employee entity."""

    employee_id: int
    name: str
    department: str