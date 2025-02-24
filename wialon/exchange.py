"""This module contains the Exchange class.

Which provides methods for importing and exporting messages from Wialon.
"""

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from wialon.errors import FormatError, NoFileReturnedError

if TYPE_CHECKING:
    from .wialon import Wialon


class Exchange:
    """The Exchange class.

    Provides methods for importing and exporting messages from Wialon.
    """

    def __init__(self, engine: "Wialon") -> None:
        """Initialize the Exchange class.

        :param engine: The Wialon engine.
        :type engine: Wialon
        """
        self._engine = engine
        self._formats = ["txt", "kml", "plt", "wln", "wlb"]

    def import_messages(
        self,
        unit_id: int,
        filepath: str,
        event_hash: str | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]] | bytes:
        """Import messages to a unit.

        :param unit_id: The ID of the unit to import messages to.
        :type unit_id: int
        :param filepath: The path to the file containing the messages to import.
        :type filepath: str
        :param event_hash: Event Hash, defaults to None
        :type event_hash: str | None, optional
        :return: The response from the Wialon API.
        :rtype: dict[str, Any] | list[dict[str, Any]] | bytes
        """
        svc = "exchange/import_messages"
        if event_hash is None:
            params: dict[str, int | str] = {
                "itemId": unit_id,
            }
        else:
            params: dict[str, int | str] = {
                "itemId": unit_id,
                "eventHash": event_hash,
            }
        path: Path = Path(filepath)
        with Path.open(path, "rb") as file:
            files = {
                "upload_file": file,
            }
            return self._engine.request(
                svc,
                params,
                sid=self._engine.auth.get_sid(),
                send_file=files,
            )

    def export_messages_by_layer(
        self,
        layer_name: str,
        file_format: str,
        filepath: str | None = None,
        *,
        compress: bool = False,
    ) -> bytes:
        """Export messages by layer name.

        :param layer_name: The name of the layer to export messages from.
        :type layer_name: str
        :param file_format: The format of the exported file. Must be one of the
        :type file_format: str
                            supported formats.
        :param filepath: The path to save the exported file. If None, the result is
        :type filepath: str | None, optional
                         returned without saving to a file, defaults to None.
        :param compress: Whether to compress the exported file, defaults to False
        :type compress: bool, optional
        :raises FormatError: If the provided file format is not supported.
        :return: The result of the export operation.
        :rtype: str
        """
        if file_format not in self._formats:
            msg = "Invalid format"
            raise FormatError(msg)

        svc = "exchange/export_messages"
        params = {
            "layerName": layer_name,
            "format": file_format,
            "compress": 1 * compress,
        }
        result = self._engine.request(
            svc,
            params,
            sid=self._engine.auth.get_sid(),
            file=True,
        )
        if filepath and isinstance(result,bytes):
            path: Path = Path(filepath)
            with Path.open(path, "wb") as f:
                f.write(result)
            return result
        if isinstance(result,bytes):
            return result
        msg = "No file returned"
        raise NoFileReturnedError(msg)

    def export_messages_by_id(
        self,
        unit_id: int,
        date_from: datetime,
        date_to: datetime,
        file_format: str,
        **kwargs: dict[str, str | bool],
    ) -> bytes:
        """Export messages by unit ID.

        :param unit_id: The ID of the unit to export messages from.
        :type unit_id: int
        :param date_from: The start date of the messages to export.
        :type date_from: datetime
        :param date_to: The end date of the messages to export.
        :type date_to: datetime
        :param file_format: The format of the exported file.
        :type file_format: str
                            Must be one of the supported formats.
        :raises FormatError: If the provided file format is not supported.
        :return: The result of the export operation.
        :rtype: bytes
        """
        filepath = kwargs.get("filepath")
        compress = kwargs.get("compress", False)
        if file_format not in self._formats:
            msg = "Invalid file format"
            raise FormatError(msg)

        svc = "exchange/export_messages"
        params = {
            "itemId": unit_id,
            "timeFrom": int(datetime.timestamp(date_from)),
            "timeTo": int(datetime.timestamp(date_to)),
            "format": file_format,
            "compress": 1 if compress else 0,
        }
        result = self._engine.request(
            svc,
            params,
            sid=self._engine.auth.get_sid(),
            file=True,
        )
        if filepath is str and result is bytes:
            path: Path = Path(filepath)
            with Path.open(path) as f:
                f.write(result)
            return result
        return b""
