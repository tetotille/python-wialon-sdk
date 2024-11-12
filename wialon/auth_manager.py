from errors import SessionException


class AuthManager:
    def __init__(self,token:str,engine):
        self.token = token
        self.engine = engine
        self._login()

    def login(self,token):
        self.token = token
        self._login()
        
    def _login(self):
        svc = "token/login"
        params = {"token":self.token,"fl":"2"}
        response = self.engine.request(svc=svc,params=params)
        
        self.host = response["host"]
        self.sid = response["eid"]
        self.api_type = response["api"]
        self.version = response[f"{self.api_type}_version"]
        self.user_name = response["user"]["nm"]
        self.user_id = response["user"]["id"]
        
    def logout(self):
        svc = "core/logout"
        if self.sid:
            response = self.engine.request(svc=svc,sid=self.sid)
            self.sid = None
            return response
        else:
            raise SessionException("There is no active session")
        
    def get_sid(self):
        return self.sid
    
    def __str__(self):
        return f"name:{self.user_name}\nsid: {self.sid}"
