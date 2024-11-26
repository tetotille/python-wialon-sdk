from .errors import SessionException


class AuthManager:
    def __init__(self,token:str,engine):
        self.token = token
        self._engine = engine
        self._login()
        self._access_types = {
            "general": 0xffff,
            "units": 0xCCF7F00000,
            "users": 0x1F00000,
            "retranslator": 0x300000,
            "resources": 0x301FFFF00000,
            "routes": 0x100000,
            "all": 0xfffffffffffffff
        }

    def login(self,token):
        self.token = token
        self._login()
        
    def _login(self):
        svc = "token/login"
        params = {"token":self.token,"fl":"2"}
        response = self._engine.request(svc=svc,params=params)
        
        self.host = response["host"]
        self._sid = response["eid"]
        self.api_type = response["api"]
        self.version = response[f"{self.api_type}_version"]
        self.user_name = response["user"]["nm"]
        self.user_id = response["user"]["id"]

    def account_detail(self,detailed:bool=False):
        """
        Retrieve account details.

        Args:
            detailed (bool, optional): If True, retrieves detailed account information. Defaults to False.

        Returns:
            dict: The account data retrieved from the service.
        """
        svc = "core/get_account_data"
        detailed = 1 if detailed else 0
        params = {"type":detailed}
        return self._engine.request(svc=svc,params=params,sid=self.get_sid())
        
    def check_access(self,itemsId:list[int],accessType:str,service_name:str="*",flags:int=0):
        """
        Check access permissions for specified items.

        Args:
            itemsId (list[int]): List of item IDs to check access for.
            accessType (str): Type of access to check. Must be one of the predefined access types:
                - general: General access
                - units: Access to units
                - users: Access to users
                - retranslator: Access to retranslator
                - resources: Access to resources
                - routes: Access to routes
                - all: Access to all
            service_name (str, optional): Name of the service requesting access. Defaults to "*".
            flags (int, optional): Flags to modify access check behavior. Defaults to 0.

        Raises:
            ValueError: If the provided accessType is not valid.

        Returns:
            dict: Response from the engine request indicating access permissions.
        """
        svc = "core/check_items_billing"
        if accessType not in self._access_types: raise ValueError(f"Invalid access type: {accessType}")
        params = {
            "itemId":itemsId,
            "accessType": flags if flags else self._access_types[accessType],
            "serviceName":service_name
        }
        return self._engine.request(svc=svc,params=params,sid=self.get_sid())
        
    def logout(self):
        svc = "core/logout"
        if self.get_sid():
            response = self._engine.request(svc=svc,sid=self.get_sid())
            self._sid = None
            return response
        else:
            raise SessionException("There is no active session")
        
    def get_sid(self):
        return self._sid
    
    def __str__(self):
        return f"name:{self.user_name}\nsid: {self.sid}"
