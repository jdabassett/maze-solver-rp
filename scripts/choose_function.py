from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Functions:
    """
    Dataclass to hold functions for retrieval
    """
    functions: dict
    default: Any

    def __getitem__(self, name: str):
        """
        Method to return function from Functions dataclass.
        :param name: str
        :return: function
        """
        return self.functions.get(name, self.default)