"""AuthManager class."""

from typing import TYPE_CHECKING, Any

from .errors import SessionExceptionError

if TYPE_CHECKING:
    from .wialon import Wialon


class AuthManager:
    """AuthManager class."""

    def __init__(self, token: str, engine: "Wialon") -> None:
        """Initialize the AuthManager class.

        :param token: The authentication token.
        :type token: str
        :param engine: The Wialon engine instance.
        :type engine: Wialon
        """
        self.token = token
        self._engine = engine
        self._access_types = {
            "general": 0xFFFF,
            "units": 0xCCF7F00000,
            "users": 0x1F00000,
            "retranslator": 0x300000,
            "resources": 0x301FFFF00000,
            "routes": 0x100000,
            "all": 0xFFFFFFFFFFFFFFF,
        }
        self.host = None
        self._sid = ""
        self.api_type = None
        self.version = None
        self.user_name = None
        self.user_id = None
        self._login()

    def login(self, token: str) -> None:
        """Login to the Wialon API.

        :param token: The authentication token.
        :type token: str
        """
        self.token = token
        self._login()

    def _login(self) -> None:
        """Login to the Wialon API."""
        svc = "token/login"
        params = {"token": self.token, "fl": "2"}
        response: dict[
            str,
            str | int | dict[str, str | int | dict[str, str | int | bool]],
        ] = (  # type: ignore[no-untyped-call]
            self._engine.request(
                svc=svc,
                params=params,
            )
        )

        self.host = response["host"]
        if isinstance(response["eid"], str):
            self._sid: str = response["eid"]
        self.api_type = response["api"]
        self.version = response[f"{self.api_type}_version"]
        if type(response["user"]) is dict:
            self.user_name = response["user"]["nm"]
            self.user_id = response["user"]["id"]

    def account_detail(
        self,
        detailed: int = 0,
    ) -> dict[str, Any] | list[dict[str, Any]] | bytes:
        """Retrieve account details from the Wialon API.

        :param detailed: Flag to indicate whether to retrieve detailed account
        :type detailed: int, optional
                         information. Defaults to 0.
        :return: Account details from the Wialon API.
        :rtype: dict
        """
        svc = "core/get_account_data"
        detailed = 1 if detailed else 0
        params = {"type": str(detailed)}
        return self._engine.request(svc=svc, params=params, sid=self.get_sid())

    def check_access(
        self,
        items_id: list[int],
        access_type: str,
        service_name: str = "*",
        flags: int = 0,
    ) -> dict[str, Any] | list[dict[str, Any]] | bytes:
        """Check access permissions for specified items.

        :param items_id: The items ID.
        :type items_id: list[int]
        :param access_type: The access type.
        :type access_type: str
        :param service_name: The service name.
        :type service_name: str, optional
        :param flags: The flags.
        :type flags: int, optional
        :return: The access permissions for the specified items.
        :rtype: dict
        """
        svc = "core/check_items_billing"
        if access_type not in self._access_types:
            msg = f"Invalid access type: {access_type}"
            raise ValueError(msg)
        params = {
            "itemId": items_id,
            "accessType": flags if flags else self._access_types[access_type],
            "serviceName": service_name,
        }
        return self._engine.request(svc=svc, params=params, sid=self.get_sid())

    def logout(self) -> dict[str, Any] | list[dict[str, Any]] | bytes:
        """Logout from the Wialon API.

        :raises SessionException: If there is no active session.
        :return: The response from the API.
        :rtype: dict[str, Any] | list[dict[str, Any]] | bytes
        """
        svc = "core/logout"
        if self.get_sid():
            response = self._engine.request(svc=svc, sid=self.get_sid())
            self._sid = ""
            return response

        msg = "There is no active session"
        raise SessionExceptionError(msg)

    def get_sid(self) -> str:
        """Get the session ID.

        :return: The session ID.
        :rtype: str
        """
        return self._sid

    def __str__(self) -> str:
        """Return the string representation of the AuthManager object.

        :return: The string representation of the AuthManager object.
        :rtype: str
        """
        return f"name:{self.user_name}\nsid: {self._sid}"
