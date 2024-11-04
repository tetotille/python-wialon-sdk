import json
import requests

from errors import validate_error


class Wialon:
    def __init__(self,api_url:str,**kwargs):
        self.api_url = api_url
        self.port = kwargs.get("port",443 if self.api_url.startswith("https") else 80)
        
    def request(self,svc:str,params:dict={},sid:str=None):
        query = {
            "svc":svc,
        }
        if sid: query["sid"] = sid
        query["params"] = str(params).replace("'",'"')
        
        response = requests.post(self.api_url,params=query)
        response = json.loads(response.content)
        validate_error(response)
        
        return response


if __name__ == "__main__":
    engine = Wialon("YOUR_API_URL_HERE")
    data = engine.request(svc="token/login",params={"token":"YOUR_API_KEY_HERE","fl":"2"})
    print(data)