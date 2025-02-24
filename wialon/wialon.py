"""The main module for the Wialon API client."""

import json
from typing import Any

import requests

from . import AuthManager, Exchange, Extra, Items, Messages, Render, validate_error


class Wialon:
    """The main class for the Wialon API client."""

    def __init__(
        self,
        api_url: str,
        api_key: str,
        **kwargs: str | int | bool,
    ) -> None:
        """Initializes the Wialon API client.

        :param api_url: the API URL to be used
        :type api_url: str
        :param api_key: the API key to be used
        :type api_key: str
        """
        self._api_url = api_url
        self._api_key = api_key
        verify_cert = kwargs.get("verify_cert", True)
        self._verify_cert: bool = verify_cert if isinstance(verify_cert, bool) else True
        self.port = kwargs.get("port", 443 if self._api_url.startswith("https") else 80)
        self._auth = AuthManager(self._api_key, self)
        self._exchange = None
        self._extra = None
        self._messages = None
        self._items = None
        self._render = None

    def request(
        self,
        svc: str,
        params: dict[str, str]
        | dict[str, str | int]
        | dict[str, dict[str, str] | int]
        | dict[str, int | dict[str, int]]
        | dict[str, int | dict[str, int | str | bool]]
        | dict[str, str | int | list[int]]
        | list[dict[str, Any]]
        | None = None,
        sid: str | None = None,
        send_file: dict[str, Any] | None = None,
        **kwargs: bool | str,
    ) -> dict[str, Any] | list[dict[str, Any]] | bytes:
        """Make a request to the Wialon API.

        :param svc: the Wialon API service to be used
        :type svc: str
        :param params: the parameters to be used, defaults to None
        :type params: dict[str, str] | dict[str, str  |  int] | dict[str, dict[str, str]
        |  int] | dict[str, int  |  dict[str, int]] | dict[str, int  |  dict[str, int
        |  str  |  bool]] | dict[str, str  |  int  |  list[int]] | list[dict[str, Any]]
        | None, optional
        :param sid: the session ID to be used, defaults to None
        :type sid: str | None, optional
        :param send_file: the file to be sent, defaults to None
        :type send_file: dict[str, Any] | None, optional
        :raises json.JSONDecodeError: Response is not a valid JSON.
        :return: the response from the Wialon API
        :rtype: dict[str, Any] | list[dict[str, Any]] | bytes
        """
        _form_data = kwargs.get("form_data", False)
        _file = kwargs.get("file", False)
        form_data = _form_data if isinstance(_form_data, bool) else False
        file_upload = _file if isinstance(_file, bool) else False

        query = {
            "svc": svc,
        }
        if sid:
            query["sid"] = sid

        if form_data:
            response = requests.post(
                self._api_url,
                json={"params": params},
                files=send_file,
                verify=self._verify_cert,
                timeout=30,
            )
        else:
            query["params"] = str(params).replace("'", '"').replace('"', '"')
            response = requests.post(
                self._api_url,
                params=query,
                files=send_file,
                verify=self._verify_cert,
                timeout=30,
            )
        if not file_upload:
            try:
                response = json.loads(response.content)
                validate_error(response)
            except json.JSONDecodeError as exc:
                msg = "Response is not a valid JSON, please verify the API URL."
                raise json.JSONDecodeError(
                    msg,
                    str(exc),
                    0,
                ) from exc

            return response
        return response.content

    @property
    def auth(self) -> AuthManager:
        """Return the AuthManager instance.

        :return: the AuthManager instance
        :rtype: AuthManager
        """
        return self._auth

    @property
    def exchange(self) -> Exchange:
        """Return the Exchange instance.

        :return: the Exchange instance
        :rtype: Exchange
        """
        if self._exchange is None:
            self._exchange = Exchange(self)
        return self._exchange

    @property
    def extra(self) -> Extra:
        """Return the Extra instance.

        :return: the Extra instance
        :rtype: Extra
        """
        if self._extra is None:
            self._extra = Extra(self)
        return self._extra

    @property
    def items(self) -> Items:
        """Return the Items instance.

        :return: the Items instance
        :rtype: Items
        """
        if self._items is None:
            self._items = Items(self)
        return self._items

    @property
    def messages(self) -> Messages:
        """Return the Messages instance.

        :return: the Messages instance
        :rtype: Messages
        """
        if self._messages is None:
            self._messages = Messages(self)
        return self._messages

    @property
    def render(self) -> Render:
        """Return the Render instance.

        :return: the Render instance
        :rtype: Render
        """
        if self._render is None:
            self._render = Render(self)
        return self._render

    def __str__(self) -> str:
        """Return the string representation of the Wialon object."""
        return f""" Wialon API Client
                    API URL: {self._api_url}
                    API Key: {self._api_key}
                    Verify Cert: {self._verify_cert}
                    Port: {self.port}

                    Auth: {self._auth}
                    Exchange: {self._exchange}
                    Extra: {self._extra}
                    Items: {self._items}
                    Messages: {self._messages}
                    Render: {self._render}

                    """
