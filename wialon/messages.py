"""Messages class which is used to interact with the Wialon messages API."""

from datetime import datetime
from typing import TYPE_CHECKING, Any

from wialon.errors import InvalidResultError

if TYPE_CHECKING:
    from .wialon import Wialon


class Messages:
    """Messages class which is used to interact with the Wialon messages API."""

    def __init__(self, engine: "Wialon") -> None:
        """Initialize the Messages class.

        :param engine: The Wialon engine to use.
        :type engine: Wialon
        """
        self._engine = engine
        self._unit_messages = {
            "data": 0x0,
            "SMS": 0x100,
            "command": 0x200,
            "event": 0x600,
            "video_usage": 0x2000,
        }
        self._resource_messages = {
            "default": 0x0,
            "notification": 0x300,
            "billing_message": 0x500,
            "SMS_for_driver": 0x900,
        }
        self._message_filter = {
            "position": 0x1,
            "input": 0x2,
            "output": 0x4,
            "state": 0x8,
            "alarm_bit": 0x10,
            "avl_driver": 0x20,
            "lbs_corrected": 0x20000,
            "wifi_position": 0x80000,
        }
        self._event_filter = {
            "violation": 0x1,
            "maitenance": 0x2,
            "route_control": 0x4,
            "maitenance_registered": 0x10,
            "filling_registered": 0x20,
        }

        self._logs = 0x1000

    def load_interval(
        self,
        item_id: int,
        time_from: datetime = datetime(1969, 12, 31, 20, 0),
        time_to: datetime = datetime(2106, 2, 7, 3, 28, 15),
        **kwargs: dict[str, int | str | bool],
    ) -> dict[str, Any]:
        """Load messages for a given item within a specified time interval.

        :param item_id: The ID of the item to load messages for.
        :type item_id: int
        :param time_from: The start time of the interval,
        :type time_from: datetime, optional
                          defaults to datetime(1969, 12, 31, 20, 0).
        :param time_to: The end time of the interval, defaults to
        :type time_to: datetime, optional
                        datetime(2106, 2, 7, 3, 28, 15).
        :param kwargs: Additional parameters for message loading.
        :type kwargs: dict[str, int | str | bool]
        :keyword message_type: The type of messages to load, defaults to "data".
        :keyword resource: The resource to use, defaults to "default".
        :keyword log: Whether to include logs, defaults to False.
        :keyword message_filter: Filter for messages, defaults to "".
        :keyword event_filter: Filter for events, defaults to "".
        :keyword mask_filter: Filter mask, defaults to 0.
        :keyword flags_mask: Mask for flags, defaults to 0xFF00.
        :keyword load_count: Number of messages to load, defaults to 0xFFFFFFFF.
        :return: A dictionary containing the loaded messages.
        :rtype: dict[str, Any]
        :raises InvalidResultError: If the request fails to fetch messages.
        """
        _mtype = kwargs.get("message_type", "data")
        _resourte = kwargs.get("resource", "default")
        _log = kwargs.get("log", False)
        _message = kwargs.get("message_filter")
        _event = kwargs.get("event_filter")
        _mask = kwargs.get("mask_filter")

        mtype = _mtype if isinstance(_mtype, str) else "data"
        resource = _resourte if isinstance(_resourte, str) else "default"
        log = _log if isinstance(_log, bool) else False
        message = _message if isinstance(_message, str) else ""
        event = _event if isinstance(_event, str) else ""
        mask = _mask if isinstance(_mask, int) else 0

        mtype = self._unit_messages[mtype]
        resource = self._resource_messages[resource]
        log = self._logs if log else 0

        message_filter = self._process_filter(
            message,
            event,
            mask,
        )
        svc = "messages/load_interval"
        params = {
            "itemId": item_id,
            "timeFrom": int(datetime.timestamp(time_from)),
            "timeTo": int(datetime.timestamp(time_to)),
            "flags": mtype | resource | log | message_filter,
            "flagsMask": kwargs.get("flags_mask", 0xFF00),
            "loadCount": kwargs.get("load_count", 0xFFFFFFFF),
        }
        for key in list(params):
            if not params[key]:
                del params[key]

        result = self._engine.request(
            svc,
            dict(params.items()),
            self._engine.auth.get_sid(),
        )

        if isinstance(result, dict) and "messages" in result:
            return result["messages"]
        msg = "Failed to fetch messages for the interval."
        raise InvalidResultError(msg)

    def load_last(
        self,
        item_id: int,
        last_time: int,
        last_count: int,
        **kwargs: dict[str, int],
    ) -> dict[str, Any]:
        """Load the last messages for a given item within a specified time interval.

        :param item_id: The ID of the item to load messages for.
        :type item_id: int
        :param last_time: The end time of the interval to load messages for.
        :type last_time: int
        :param last_count: The number of messages to load.
        :type last_count: int
        :param kwargs: Additional parameters for the request.
        :type kwargs: dict[str, int]
        :keyword flags: Optional flags for the request.
        :keyword flags_mask: Optional mask for the flags.
        :keyword load_count: Optional count of messages to load.
        :return: A dictionary containing the loaded messages.
        :rtype: dict[str, Any]
        :raises InvalidResultError: If the request fails to fetch messages.
        """
        flags = kwargs.get("flags", 0)
        flags_mask = kwargs.get("flags_mask", 0)
        load_count = kwargs.get("load_count", 0)

        svc = "messages/load_last"
        params = {
            "itemId": item_id,
            "lastTime": last_time,
            "lastCount": last_count,
            "flags": flags,
            "flagsMask": flags_mask,
            "loadCount": load_count,
        }
        for key in list(params):
            if not params[key]:
                del params[key]

        result = self._engine.request(svc, params, self._engine.auth.get_sid())
        if isinstance(result, dict):
            return result
        msg = "Failed to fetch messages for the interval."
        raise InvalidResultError(msg)

    def _process_filter(self, message: str, event: str, mask: int | None) -> int:
        # TODO(tetotille): create mask filter  # noqa: FIX002, TD003
        # No Issue
        message_filter = 0
        if message:
            for _m in message.split(","):
                m = _m.strip()
                if m in self._message_filter:
                    message_filter |= self._message_filter[m]

        event_filter = 0
        if event:
            for _e in event.split(","):
                e = _e.strip()
                if e in self._event_filter:
                    event_filter |= self._event_filter[e]

        mask_filter = mask if mask is not None else 0

        return message_filter | event_filter | mask_filter
