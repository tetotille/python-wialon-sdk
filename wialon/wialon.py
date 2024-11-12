import json
import requests

from auth_manager import AuthManager
from errors import validate_error
from messages import Messages
import os


class Wialon:
    def __init__(self,api_url:str,api_key:str,**kwargs):
        self._api_url = api_url
        self._api_key = api_key
        self.port = kwargs.get("port",443 if self._api_url.startswith("https") else 80)
        self._auth = AuthManager(self._api_key,self)
        self._messages = None
        
    def request(self,svc:str,params:dict={},sid:str=None):
        query = {
            "svc":svc,
        }
        if sid: query["sid"] = sid
        query["params"] = str(params).replace("'",'"')
        
        response = requests.post(self._api_url,params=query)
        response = json.loads(response.content)
        validate_error(response)
        
        return response
    
    @property
    def auth(self):
        if self._auth is None:
            self._auth = AuthManager(self._api_key,self)
        return self._auth
    
    @property
    def messages(self):
        if self._messages is None:
            self._messages = Messages(self)
        return self._messages


