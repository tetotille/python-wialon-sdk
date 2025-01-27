import json
import requests

from . import AuthManager,Exchange,Extra,Items,Messages,Render,validate_error

from typing import Any,Dict,List,Optional,Union

class Wialon:
    def __init__(self,api_url:str,api_key:str,**kwargs: Any):
        self._api_url = api_url
        self._api_key = api_key
        self._verify_cert = kwargs.get("verify_cert",None)
        self.port = kwargs.get("port",443 if self._api_url.startswith("https") else 80)
        self._auth = AuthManager(self._api_key,self)
        self._exchange = None
        self._extra = None
        self._messages = None
        self._items = None
        self._render = None
        
    def request(self,svc:str,params:Union[Dict[str,str],List[Dict[str,Any]]]={},sid:Optional[str]=None,form_data:bool=False,file:bool=False,send_file:Optional[Dict[str, Any]]={}) -> Union[Dict[str,Any],List[Dict[str,Any]],bytes]:
        """
        Sends a request to the Wialon API.
        Args:
            svc (str): The service name to be requested.
            params (Union[Dict[str, str], List[Dict[str, Any]]], optional): The parameters to be sent with the request. Defaults to {}.
            sid (Optional[str], optional): The session ID. Defaults to None.
            form_data (bool, optional): Whether to send the data as form data. Defaults to False.
            file (bool, optional): Whether the response is expected to be a file. Defaults to False.
            send_file (Optional[Dict[str, Any]], optional): The file data to be sent with the request. Defaults to {}.
        Returns:
            Union[Dict[str, Any], List[Dict[str, Any]], bytes]: The response from the API. If `file` is False, the response is parsed as JSON and returned as a dictionary or list. If `file` is True, the raw bytes of the response content are returned.
        Raises:
            json.JSONDecodeError: If the response content is not a valid JSON and `file` is False.
        """
        query = {
            "svc":svc,
        }
        if sid: query["sid"] = sid
        
        if form_data:
            response = requests.post(self._api_url, json={"params": params}, files=send_file, verify=self._verify_cert)
        else:
            query["params"] = str(params).replace("'",'\"').replace('"','\"')
            response = requests.post(self._api_url,params=query,files=send_file,verify=self._verify_cert)
        if not file:
            try:
                response = json.loads(response.content)
                validate_error(response)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError("Response is not a valid JSON, please verify the API URL.", str(e), 0)
        
            return response
        else:
            return response.content
    
    @property
    def auth(self):
        return self._auth
    
    @property
    def exchange(self):
        if self._exchange is None:
            self._exchange = Exchange(self)
        return self._exchange
    
    @property
    def extra(self):
        if self._extra is None:
            self._extra = Extra(self)
        return self._extra
    
    @property
    def items(self):
        if self._items is None:
            self._items = Items(self)
        return self._items
    
    @property
    def messages(self):
        if self._messages is None:
            self._messages = Messages(self)
        return self._messages
    
    @property
    def render(self):
        if self._render is None:
            self._render = Render(self)
        return self._render