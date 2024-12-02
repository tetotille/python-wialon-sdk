import json
import requests

from . import AuthManager,Exchange,Items,Messages,Render,validate_error


class Wialon:
    def __init__(self,api_url:str,api_key:str,**kwargs):
        self._api_url = api_url
        self._api_key = api_key
        self.port = kwargs.get("port",443 if self._api_url.startswith("https") else 80)
        self._auth = AuthManager(self._api_key,self)
        self._exchange = None
        self._messages = None
        self._items = None
        self._render = None
        
    def request(self,svc:str,params:dict={},sid:str=None,form_data=False,file=False):
        query = {
            "svc":svc,
        }
        if sid: query["sid"] = sid
        
        if form_data:
            response = requests.post(self._api_url,json={"params":params})
        else:
            query["params"] = str(params).replace("'",'\"').replace('"','\"')
            response = requests.post(self._api_url,params=query)
        if not file:
            response = json.loads(response.content)
            validate_error(response)
        
            return response
        else:
            return response.content
    
    @property
    def auth(self):
        if self._auth is None:
            self._auth = AuthManager(self._api_key,self)
        return self._auth
    
    @property
    def exchange(self):
        if self._exchange is None:
            self._exchange = Exchange(self)
        return self._exchange
    
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


