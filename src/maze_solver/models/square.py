from dataclasses import dataclass

from border import Border
from role import Role


@dataclass(frozen=True)
class Square:
    """
    Immutable dataclass containing all square information
    index, row, column, border, and role
    """
    index: int
    row: int
    column: int
    border: Border
    role: Role = Role.NONE
