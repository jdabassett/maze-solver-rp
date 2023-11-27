# parent to data classes that are expected by only contain and modify their own data
from dataclasses import dataclass

from src.maze_solver.models.border import Border
from src.maze_solver.models.role import Role


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
