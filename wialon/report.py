"""Reports module."""
from datetime import datetime
from time import sleep
from typing import TYPE_CHECKING, Any

from loguru import logger

if TYPE_CHECKING:
    from .wialon import Wialon

class Report:
    """Reports class.

    :ivar wialon _engine: The Wialon object.
    :cvar dict _statuses: The report statuses.
    """

    def __init__(self, engine:"Wialon") -> None:
        """Initialize the Reports class.

        :param wialon wialon: The Wialon object.
        """
        self._engine = engine
        self._statuses = {1: "In a queue",
                          2: "Proceed",
                          4: "Done",
                          8: "Canceled",
                          16: "Invalid report (no such report)"}
        self._has_result = False
        self._export_formats = {
            "html": 1,
            "pdf": 2,
            "xls": 4,
            "xlsx": 8,
            "xml": 16,
            "csv": 32,
        }
        self._page_width = {
            "fixed": 0,
            "compact": 1,
            "no wrap": 2,
        }
        self._pages_sizes = ["a4","a3","legal","letter"]

    def apply_result(self) -> dict[str,Any]:
        """Retrieve the report result.

        :raises ValueError: If the report result cannot be retrieved.
        :return: The report result.
        :rtype: dict[str,Any]
        """
        svc = "report/apply_report_result"
        params = {}
        response = self._engine.request(svc=svc,
                                        params=params,
                                        sid=self._engine.auth.get_sid())
        if isinstance(response, dict):
            logger.info("Report result applied.")
            self._has_result = True
            return response

        logger.error("The request response is not dict")
        logger.debug(f"Request: {params}, Response: {response}")
        msg = "Failed to retrieve report result."
        raise ValueError(msg)

    def get_result(self,
                   table_index:int=0,
                   index_from:int=0,
                   index_to:int=0,
                   **kwargs:bool) -> list[dict[str,Any]]:
        """Obtain the report result.

        :param table_index: The index of the previous execution table, defaults to 0
        :type table_index: int, optional
        :param index_from: The index of the row from where it will be taken into account,
        :type index_from: int, optional
        defaults to 0
        :param index_to: The index to the row that will be taken into account,
        :type index_to: int, optional
        defaults to 0
        :param multi_level: The indicator of whether the sub -levels must be recovered,
        :type multi_level: bool, optional
        defaults to False
        :raises ValueError: If the report result cannot be recovered.
        :return: The result of the report.
        :rtype: dict[str,Any]
        """
        if not self._has_result:
            logger.error("No report result to retrieve. First generate a report.")
            msg = "No report result to retrieve. First generate a report."
            raise BufferError(msg)

        multi_level = kwargs.get("multi_level", False)

        svc = "report/get_result_rows"
        params = {
            "tableIndex": table_index,
            "indexFrom": index_from,
            "indexTo": index_to,
        }
        response = self._engine.request(svc=svc,
                                        params=params,
                                        sid=self._engine.auth.get_sid())

        if not isinstance(response, list):
            logger.error("The request response is not dict")
            logger.debug(f"Request: {params}, Response: {response}")
            msg = "Failed to retrieve report result."
            raise TypeError(msg)

        if multi_level:
            return self._get_sub_rows(table_index, list(range(index_from, index_to)))

        return response

    def _get_sub_rows(self,
                      table_index:int,
                      row_index:int|list[int],
                      ) -> list[dict[str,Any]]:
        """Retrieve the sub rows of a report.

        :param int table_index: The table index.
        :param int row_index: The row index.
        :return: The sub rows of the report.
        :rtype: list[dict[str,Any]]|list[list[dict[str,Any]]]
        """
        if isinstance(row_index, int):
            svc = "report/get_result_subrows"
            params = {
                "tableIndex": table_index,
                "rowIndex": row_index,
            }
            response = self._engine.request(svc=svc,
                                        params=params,
                                        sid=self._engine.auth.get_sid())
            if isinstance(response, list):
                return response
            logger.error("The request response is not list")
            logger.debug(f"Request: {params}, Response: {response}")
            msg = "Failed to retrieve sub rows."
            raise ValueError(msg)

        params = [{"svc": "report/get_result_subrows",
                   "params": {"tableIndex": table_index,
                              "rowIndex": x}} for x in row_index]

        response = self._engine.extra.batch(params)

        return [
                item
                for sublist in response
                for item in sublist
                if isinstance(item, dict)
            ]

    def execute(self,
                object_id:int|list[int],
                resource_id:int,
                template_id:int,
                **kwargs:datetime|int|str) -> str|dict[str,Any] :
        """Execute a report.

        :param int|list[int] object_id: Object ID or list of object IDs.
        :param int resource_id: Resource ID.
        :param int template_id: Template ID.
        :raises ValueError: If the report generation fails.
        :param datetime date_from: The start date. Default is the first day of the month.
        :param datetime date_to: The end date. Default is today.
        :param int object_sec_id: The object sec ID. Default is 0.
        :param int flags: The flags. Default is 0x1000000.
        :param str report_template: The report template. Default is "".
        :param bool remote_exec: The remote execution flag. Default is True.
        :param bool async_wait: The async wait flag. Default is True.
        :return: The report result.
        :rtype: str
        :return: The dict with the report results.
        :rtype: dict[str,Any]
        """
        logger.info("Executing report.")
        logger.debug(f"""Object ID: {object_id},
                     Resource ID: {resource_id},
                     Template ID: {template_id}""")
        # Get extra params
        now = datetime.now()
        date_from = kwargs.get("date_from",
                               datetime(now.year, now.month, now.day))
        date_to = kwargs.get("date_to",
                             datetime(now.year, now.month, now.day,23,59,59))

        object_sec_id = kwargs.get("object_sec_id", 0)
        flags = kwargs.get("flags", 0x1000000)
        report_template = kwargs.get("report_template", "")
        remote_exec = kwargs.get("remote_exec", True)
        async_wait = kwargs.get("async_wait", True)
        # Data Validation
        ## Date Validation
        if not isinstance(date_from, datetime) or not isinstance(date_to, datetime):
            date_from = datetime(now.year, now.month, now.day)
            date_to = datetime(now.year, now.month, now.day,23,59,59)

        date_from_ts = int(date_from.timestamp())
        date_to_ts = int(date_to.timestamp())

        ## Object ID Validation
        if isinstance(object_id, int):
            first_object_id = object_id
            object_list = []
        else:
            first_object_id = object_id[0]
            object_list = object_id[1:]


        ## Object sec id validation
        if not isinstance(object_sec_id, int):
            object_sec_id = 0

        ## Flags Validation
        if not isinstance(flags, int):
            flags = 0x1000000

        ## Report Template Validation
        if not isinstance(report_template, str):
            report_template = ""

        ## Remote Exec Validation
        if not isinstance(remote_exec, bool):
            remote_exec = True

        # Prepare the request
        svc = "report/exec_report"
        params = {
            "reportResourceId": resource_id,
            "reportTemplateId": template_id,
            "reportObjectId": first_object_id,
            "reportObjectSecId": object_sec_id,
            "reportObjectIdList": object_list,
            "interval": {
                "from": date_from_ts,
                "to": date_to_ts,
                "flags": flags,
            },
            "remoteExec": 1 if remote_exec else 0,
            "reportTemplate": report_template,
        }
        logger.debug(f"Request: {params}")

        # Request and results
        response = self._engine.request(svc=svc,
                                      params=params,
                                      sid=self._engine.auth.get_sid())

        if isinstance(response, dict):
            self._has_result = False
            result: dict[str,int] = response
            if "remoteExec" in result and result["remoteExec"] == 1:

                # Wait for the report to be generated
                if not async_wait:
                    response = self.status()
                    done = "4"
                    while response["code"] != done:
                        response = self.status()
                        logger.info(f"Waiting status: {response}")
                    response = self.apply_result()
                    logger.debug(response)
                    return response

                return "Report is being generated."
        msg = "Report generation failed."
        raise ValueError(msg)

    def export_result(self,file_format:str, **kwargs:bool|int|str) -> bytes:
        """Export the report result.

        :param str file_format: The file format.
        :param bool,optional compress: The compress flag. Default is True.
        :param str,optional page_orientation: The page orientation. Default is landscape.
        [landscape, portrait]
        :param str,optional page_size: The page size. Default is a4.
        [a4, a3, legal, letter]
        :param str,optional page_width: The page width. Default is fixed.
        [fixed, compact, no wrap]
        :param str,optional coding: The coding. Default is utf8. [utf8, cp1251]
        :param str,optional delimiter: The delimiter. Default is comma. [(,), (;)]
        :param bool,optional headings: The headings flag. Default is False.
        :param bool,optional attach_map: The attach map flag. Default is False.
        :param bool,optional extend_bounds: The extend bounds flag. Default is False.
        :param bool,optional hide_map_basis: The hide map basis flag. Default is False.
        :raises BufferError: If there is no report result to export.
        :raises ValueError: If the export format is invalid.
        :raises TypeError: If the report result cannot be exported.
        :return: The exported report result.
        :rtype: bytes
        """
        if not self._has_result:
            msg = "No report result to export. First generate a report."
            raise BufferError(msg)
        if file_format not in self._export_formats:
            msg = "Invalid export format."
            raise ValueError(msg)

        svc = "report/export_result"

        _compress = kwargs.get("compress", True)
        compress = 1 if _compress else 0
        attach_map = 0
        page_orientation = "landscape"
        page_size = "a4"
        page_width = 0
        coding = "utf8"
        delimiter = "comma"
        headings = 0
        extend_bounds = 0
        hide_map_basis = 0
        output_filename = None

        if file_format == "csv":
            _coding = self._validate_data(
                kwargs.get("coding", "utf8"), ["utf8", "cp1251"], "in",
            )
            coding = _coding

            _delimiter = self._validate_data(kwargs.get("delimiter", ","),[",",";"],"in")
            delimiter = "comma" if _delimiter == "," else "semicolon"

            _headings = self._validate_data(kwargs.get("headings", False),bool)
            headings = 1 if _headings else 0

        if file_format == "pdf":
            _page_orientation = self._validate_data(
                kwargs.get("page_orientation", "landscape"),["landscape","portrait"],"in",
            )
            page_orientation = _page_orientation

            _page_size = self._validate_data(
                kwargs.get("page_size", "a4"),self._pages_sizes,"in",
            )
            page_size = _page_size

            _page_width = self._validate_data(
                kwargs.get("page_width", "fixed"),self._page_width,"in",
            )
            page_width = self._page_width.get(_page_width)

        if file_format in ("pdf", "html"):
            _attach_map = self._validate_data(kwargs.get("attach_map", False),bool)
            attach_map = 1 if _attach_map else 0

            _extend_bounds = self._validate_data(kwargs.get("extend_bounds", False),bool)
            extend_bounds = 1 if _extend_bounds else 0

            _hide_map_basis = self._validate_data(
                kwargs.get("hide_map_basis", False),bool,
            )
            hide_map_basis = 1 if _hide_map_basis else 0

        params = {
            "format": self._export_formats[file_format],
            "compress": compress,
            "pageOrientation": page_orientation,
            "pageSize": page_size,
            "pageWidth": page_width,
            "coding": coding,
            "delimiter": delimiter,
            "headings": headings,
            "attachMap": attach_map,
            "extendBounds": extend_bounds,
            "hideMapBasis": hide_map_basis,
            "outputFileName": output_filename,
        }
        response = self._engine.request(svc=svc,
                                        params=params,
                                        sid=self._engine.auth.get_sid())
        if isinstance(response, bytes):
            return response
        msg = "Failed to export report result."
        raise TypeError(msg)

    def status(self) -> dict[str,str]:
        """Retrieve the report status.

        :raises ValueError: If the report status cannot be retrieved.
        :return: The report status.
        :rtype: dict[str,str]
        """
        sleep(2)
        svc = "report/get_report_status"
        params = {}
        response = self._engine.request(svc=svc,
                                      params=params,
                                      sid=self._engine.auth.get_sid())
        if isinstance(response, dict) and "status" in response:
            code = int(response["status"])
            return {"code":response["status"],
                    "result":self._statuses[code]}
        msg = "Failed to retrieve report status."
        raise ValueError(msg)

    @staticmethod
    def _validate_data(data:Any,data_val:Any,validation_type:str="equal") -> Any:  # noqa: ANN401
        """Validate the data.

        :param data: The data to validate.
        :type data: Any
        :param validation_type: The validation type.
        :type validation_type: str
        :raises ValueError: If the data is invalid.
        """
        if validation_type == "equal" and not isinstance(data, data_val):
            msg = f"Invalid data: {data}"
            raise TypeError(msg)

        if validation_type == "in" and data not in data_val:
            msg = f"Invalid data: {data}"
            raise ValueError(msg)

        return data
