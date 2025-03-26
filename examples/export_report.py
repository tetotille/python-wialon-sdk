"""Export report example."""
# ruff: noqa: T201

import os
from datetime import datetime

from wialon import Wialon

if __name__ == "__main__":
    token = os.getenv("WIALON_TOKEN")
    url = os.getenv("WIALON_URL")
    user_name = os.getenv("WIALON_USER_NAME")
    report_name = os.getenv("WIALON_REPORT_NAME")
    _object_list = os.getenv("WIALON_OBJECT_LIST")

    if not token or not url or not user_name or not report_name or not _object_list:
        msg = "Wialon token and url must be provided."
        raise ValueError(msg)
    object_list = [int(x) for x in _object_list.split(",")]

    wialon = Wialon(url, token,logging="INFO")
    resources = wialon.items.search(item_type="resource",
                        prop_name="avl_resource",
                        sort_type="avl_resource",
                        flags=0x1+0x2000)

    reports = next(x for x in resources if x.get("nm") == user_name)
    _resource_id = reports.get("id")
    resource_id = (
        _resource_id if isinstance(_resource_id, int) else (
            int(_resource_id) if isinstance(_resource_id, str) else 0
            )
        )
    report = next(x for x in reports.get("rep").values() if x.get("n") == report_name) # type: ignore[assignment]
    report_template_id = report.get("id")

    results = wialon.report.execute(object_list,
                                    resource_id,
                                    report_template_id,
                                    date_from=datetime(2025, 3, 1),
                                    date_to=datetime.now(),
                                    async_wait = False)
    if not isinstance(results, dict):
        msg = "Invalid response from the server."
        raise TypeError(msg)

    headers = results["reportResult"]["tables"][0]["header"]
    results = wialon.report.get_result(
        index_to=results["reportResult"]["tables"][0]["rows"],
        multi_level=True,
    )
    print(headers)
    print(results)
    """The result contemplates the Headers and Results variables;Headers contains
    The names of the columns while results contains all the results.

    Headers is a string list with the names of the columns
    results has the following structure:
    list [dict [dict [str, Any]]] (at least the usable part)

    To access the data list is done as follows

    >>> results [i] ["c"]
    ['1.1', 'Tecnoedil CG-01001', {'T': '2025-03-04 10:09:17', ...}, ...]
    """
