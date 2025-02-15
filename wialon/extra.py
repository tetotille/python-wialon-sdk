"""This module contains the Extra class."""

from typing import TYPE_CHECKING, Any
from typing import Any as Wialon

if TYPE_CHECKING:
    from . import Wialon


class Extra:
    """The Extra class is used to perform extra requests to the Wialon API."""

    def __init__(self, engine: "Wialon") -> None:
        """Initialize the Extra class.

        :param engine: The Wialon object.
        :type engine: Wialon
        """
        self._engine = engine

    def batch(self, params: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Perform a batch request.

        Parameters
        ----------
        params : list of dict
            The parameters for each request in the batch.

        Returns:
        -------
        list of dict
            The results of each request in the batch.
        """
        response = self._engine.request(
            "core/batch",
            params,
            self._engine.auth.get_sid(),
        )

        if not isinstance(response, list):
            msg = "Invalid response from the server."
            raise TypeError(msg)
        result: list[dict[str, Any]] = response
        return result
