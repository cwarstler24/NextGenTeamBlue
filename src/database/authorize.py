from enum import Enum


class Role(Enum):
    """
    Roles for users in the database.
        Manager: Can add, update, and delete resources.
        Employee: Can only query resources.
        Other: Has no access to resources.
    """
    MANAGER = "Manager"
    EMPLOYEE = "Employee"
    OTHER = "Other"


def can_read(role: Role) -> bool:
    match role:
        case Role.MANAGER:
            return True
        case Role.EMPLOYEE:
            return True
        case _:
            return False


def can_write(role: Role) -> bool:
    match role:
        case Role.MANAGER:
            return True
        case _:
            return False
