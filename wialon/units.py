"""Units Module.

This is a incomplete and temporal module
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .wialon import Wialon


class Unit:
    """Unit Class."""

    def __init__(self, data: dict[str, int | str]) -> None:
        """__init__. Constructor.

        :param data: data
        :type data: dict[str, int  |  str]
        """
        self._measure_units = [
            "System International",
            "United States",
            "Imperial",
            "Metric with Gallons",
        ]
        self._data = data
        self.measure_unit: str = self._measure_units[int(data["mu"])]
        self.name = data["nm"]
        self.cls = "unit"  # Superclass ID
        self.id = self._data["id"]

    def __str__(self) -> str:
        """__str__. String representation.

        :return: data
        :rtype: str
        """
        return f"Name: {self.name}\nid: {self.id}\nUnitType: {self.cls}"

    def __eq__(self, other: object) -> bool:
        """__eq__. Equal operator.

        :param other: Unit object
        :type other: object
        :return: True if the id is the same
        :rtype: bool
        """
        if isinstance(other, Unit):
            return self.id == other.id
        return False


class Units:
    """Units Class."""

    def __init__(self, engine: "Wialon") -> None:
        """__init__. Constructor."""
        self._engine = engine
