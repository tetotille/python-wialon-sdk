"""Items module for Wialon API."""

from datetime import datetime
from typing import TYPE_CHECKING, Any

from .errors import InvalidInputError, InvalidResultError, ParameterError

if TYPE_CHECKING:
    from .wialon import Wialon


class Items:
    """Items class for Wialon API."""

    def __init__(self, engine: "Wialon") -> None:
        """__init__ method for Items class.

        :param engine: Wialon object
        :type engine: Wialon
        """
        self._engine = engine
        self._items_type: dict[str, str] = {
            "hardware": "avl_hw",
            "resource": "avl_resource",
            "retranslator": "avl_retranslator",
            "unit": "avl_unit",
            "unit_group": "avl_unit_group",
            "user": "user",
            "route": "avl_route",
        }

    def search(
        self,
        item_id: int | None = None,
        item_type: str | None = None,
        date_from: datetime = datetime(1969, 12, 31, 20, 0),
        date_to: datetime = datetime(2106, 2, 7, 3, 28, 15),
        by: str = "property",
        **kwargs: dict[str, int | str],
    ) -> list[dict[str, Any]]:
        """Search for items based on various criteria.

        :param item_id: The ID of the item to search for (used when `by` is "id").
        :type item_id: int, optional
        :param item_type: The type of item to search for (used when `by` is "property").
        :type item_type: str, optional
        :param date_from: The start date for the search range (used when `by`
        :type date_from: datetime
                          is "property").
        :param date_to: The end date for the search range (used when `by` is "property").
        :type date_to: datetime
        :param by: The search method, either "property" or "id".
        :type by: str
        :param kwargs: Additional search parameters.
        :type kwargs: dict[str, int | str]
        :return: A list of dictionaries containing the search results.
        :rtype: list[dict[str, Any]]
        :raises InvalidInputError: If an invalid `item_type` is provided.
        :raises ParameterError: If required parameters are missing or invalid.
        :raises InvalidResultError: If the search result is invalid or unexpected.
        """
        _flags = kwargs.get("flags", 0x1)
        _force = kwargs.get("force", 0)
        _prop_name = kwargs.get("prop_name", "sys_name")
        _prop_value_mask = kwargs.get("prop_value_mask", "*")
        _sort_type = kwargs.get("sort_by", "")

        # Set the params
        flags: int = _flags if _flags and isinstance(_flags, int) else 0x1
        force: int = _force if _force and isinstance(_force, int) else 0
        prop_name: str = (
            _prop_name if _prop_name and isinstance(_prop_name, str) else "sys_name"
        )
        prop_value_mask: str = (
            _prop_value_mask if _prop_value_mask and isinstance(_prop_value_mask, str)
            else "*"
        )
        sort_type = _sort_type if _sort_type and isinstance(_sort_type, str) else ""

        svc = "core/search_item"

        ### By Property
        if by == "property":
            svc = svc + "s"
            if item_type not in self._items_type:
                msg = "Please send a valid 'item_type'"
                raise InvalidInputError(msg)

            if not item_type:
                msg = """For property you need the 'item_type', 'date_from' and 'date_to'
                parameters"""
                raise ParameterError(msg)

            params: dict[str, dict[str, str] | int] = {
                "spec": {
                    "itemsType": self._items_type[item_type],
                    "propName": prop_name,
                    "propValueMask": prop_value_mask,
                    "sortType": sort_type,
                },
                "force": force,
                "flags": flags,
                "from": int(datetime.timestamp(date_from)),
                "to": int(datetime.timestamp(date_to)),
            }

        ### By ID
        elif by == "id":
            if not item_id:
                msg = "The item_id parameter must enter"
                raise ParameterError(msg)
            params = {
                "id": item_id,
                "flags": flags,
            }

        else:
            msg = "The 'by' or 'property' parameter must be"
            raise ParameterError(msg)
        result = self._engine.request(svc, params, self._engine.auth.get_sid())
        if not result:
            msg = "No data found"
            raise InvalidResultError(msg)

        if isinstance(result, dict):
            result = result["items"]
        elif isinstance(result, bytes):
            msg = "Unexpected bytes response"
            raise InvalidResultError(msg)

        return result
