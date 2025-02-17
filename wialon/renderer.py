"""Render class for creating and removing layers on the Wialon map."""

from datetime import datetime
from typing import TYPE_CHECKING, Any

from .errors import InvalidInputError

if TYPE_CHECKING:
    from .wialon import Wialon


class Render:
    """Class for creating and removing layers on the Wialon map."""

    def __init__(self, engine: "Wialon") -> None:
        """Initialize the Render class.

        :param engine: The Wialon object.
        :type engine: Wialon
        """
        self._engine = engine

    def create_message_layer(
        self,
        item_id: int,
        date_from: datetime,
        date_to: datetime,
        **kwargs: dict[str, bool | int | str],
    ) -> dict[str, Any]:
        """Create a message layer with specified parameters.

        :param item_id: The ID of the item.
        :type item_id: int
        :param date_from: The start date and time for the message layer.
        :type date_from: datetime
        :param date_to: The end date and time for the message layer.
        :type date_to: datetime
        :param kwargs: Additional optional parameters.
        :type kwargs: dict[str, bool | int | str]

        :keyword bool trip_detector: Enable trip detection (default: False).
        :keyword str track_color: Color of the track (default: "cc0000ff").
        :keyword int track_width: Width of the track (default: 4).
        :keyword bool arrows: Display arrows on the track (default: True).
        :keyword bool points: Display points on the track (default: True).
        :keyword str point_color: Color of the points (default: "cc0000ff").
        :keyword bool annotations: Display annotations (default: False).
        :keyword bool grouping_markers: Enable grouping markers (default: False).
        :keyword bool numbering_for_markers: Enable numbering for markers (default: False)
        :keyword bool events_markers: Enable event markers (default: False).
        :keyword bool fillings: Enable fillings (default: False).
        :keyword bool images: Enable images (default: False).
        :keyword bool parkings: Enable parkings (default: False).
        :keyword bool speedings: Enable speedings (default: False).
        :keyword bool stops: Enable stops (default: False).
        :keyword bool thefts: Enable thefts (default: False).
        :keyword bool video_markers: Enable video markers (default: False).

        :return: The response from the engine request.
        :rtype: dict
        """
        _trip_detector = kwargs.get("trip_detector", False)
        _track_color = kwargs.get("track_color", "cc0000ff")
        _track_width = kwargs.get("track_width", 4)
        _arrows = kwargs.get("arrows", True)
        _points = kwargs.get("points", True)
        _point_color = kwargs.get("point_color", "cc0000ff")
        _annotations = kwargs.get("annotations", False)
        _group_markers = kwargs.get("grouping_markers", False)
        _numbering_markers = kwargs.get("numbering_for_markers", False)
        _events_markers = kwargs.get("events_markers", False)
        _fillings = kwargs.get("fillings", False)
        _images = kwargs.get("images", False)
        _parkings = kwargs.get("parkings", False)
        _speedings = kwargs.get("speedings", False)
        _stops = kwargs.get("stops", False)
        _thefts = kwargs.get("thefts", False)
        _video_markers = kwargs.get("video_markers", False)

        trip_detector = _trip_detector if isinstance(_trip_detector, bool) else False
        track_color = _track_color if isinstance(_track_color, str) else "cc0000ff"
        track_width = _track_width if isinstance(_track_width, int) else 4
        arrows = _arrows if isinstance(_arrows, bool) else True
        points = _points if isinstance(_points, bool) else True
        point_color = _point_color if isinstance(_point_color, str) else "cc0000ff"
        annotations = _annotations if isinstance(_annotations, bool) else False
        group_marker = 1 if _group_markers else 0
        number_marker = 1 if _numbering_markers else 0
        event_marker = 1 if _events_markers else 0
        fillings = 1 if _fillings else 0
        images = 1 if _images else 0
        parkings = 1 if _parkings else 0
        speedings = 1 if _speedings else 0
        stops = 1 if _stops else 0
        thefts = 1 if _thefts else 0
        video_markers = 1 if _video_markers else 0

        name = "messages"
        svc = "render/create_messages_layer"
        flags = (
            0x1 * group_marker
            | 0x2 * number_marker
            | 0x4 * event_marker
            | 0x8 * fillings
            | 0x10 * images
            | 0x20 * parkings
            | 0x40 * speedings
            | 0x80 * stops
            | 0x100 * thefts
            | 0x200 * video_markers
        )
        params = {
            "layerName": name,
            "itemId": item_id,
            "timeFrom": int(date_from.timestamp()),
            "timeTo": int(date_to.timestamp()),
            "tripDetector": 1 * trip_detector,
            "trackColor": track_color,
            "trackWidth": track_width,
            "arrows": 1 * arrows,
            "points": 1 * points,
            "pointColor": point_color,
            "annotations": 1 * annotations,
            "flags": flags,
        }

        result = self._engine.request(
            svc=svc,
            params=params,
            sid=self._engine.auth.get_sid(),
        )
        if isinstance(result, dict):
            return result
        msg = f"Failed to create message layer for item ID {item_id}."
        raise InvalidInputError(msg)

    def remove_layer(self, name: str) -> bool:
        """Remove a layer from the map.

        :param name: The name of the layer to remove.
        :type name: str
        :return: True if the layer was removed successfully, False otherwise.
        :rtype: bool
        """
        svc = "render/remove_layer"
        params = {"layerName": name}
        try:
            self._engine.request(svc=svc, params=params, sid=self._engine.auth.get_sid())
        except InvalidInputError:
            return False
        return True
