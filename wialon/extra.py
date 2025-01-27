from typing import TYPE_CHECKING, Any,Any as Wialon, Dict, List

if TYPE_CHECKING:
    from . import Wialon

class Extra:
    def __init__(self,engine:Wialon):
        self._engine = engine

    def batch(self,params:List[Dict[str,Any]]) -> List[Dict[str,Any]]:
        """
        Perform a batch request.

        Parameters
        ----------
        params : list of dict
            The parameters for each request in the batch.

        Returns
        -------
        list of dict
            The results of each request in the batch.
        """
        result = self._engine.request("core/batch",params,self._engine.auth.get_sid())
        if type(result) != list:
            raise ValueError("Invalid response from the server.")
        return result