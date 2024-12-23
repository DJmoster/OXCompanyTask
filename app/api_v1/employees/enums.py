from enum import Enum


class EmployeePosition(str, Enum):
    SOFTWARE_ENGINEER = 'Software Engineer'
    DATA_SCIENTIST = 'Data Scientist'
    HUMAN_RESOURCES = 'Human Resources'
