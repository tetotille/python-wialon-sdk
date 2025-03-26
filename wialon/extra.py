"""This module contains the Extra class."""

from typing import TYPE_CHECKING, Any
from typing import Any as Wialon

from wialon.errors import (
    InvalidInputError,
    ReachedLimitOfConcurrentRequestsError,
    UnknownError,
)

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

    def batch(self,
              params: list[dict[str, Any]],
              ) -> list[dict[str, Any]]|list[list[dict[str,Any]]]:
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
        try:
            response = self._engine.request(
                "core/batch",
                params,
                self._engine.auth.get_sid(),
                timeout=60*5,
            )
        except UnknownError as exc:
            msg = "The returned result is too large."
            raise ValueError(msg) from exc
        except InvalidInputError as exc:
            msg = "Wrong input parameters."
            raise InvalidInputError(msg) from exc
        except ReachedLimitOfConcurrentRequestsError as exc:
            msg = "The flag is 1 and have 1 error in one of the requests."
            raise ReachedLimitOfConcurrentRequestsError(msg) from exc

        if not isinstance(response, list):
            msg = "Invalid response from the server."
            raise TypeError(msg)
        result: list[dict[str, Any]] = response
        return result
