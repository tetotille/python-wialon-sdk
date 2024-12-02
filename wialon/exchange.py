from datetime import datetime

class FormatException(Exception):
    """Error code 2015: Invalid format"""
    pass

class Exchange:
    def __init__(self,engine):
        self._engine = engine
        self._formats = ["txt","kml","plt","wln","wlb"]
    
    def export_messages_by_layer(self,layer_name:str,file_format:str,filepath:str=None,compress:bool=False):
        """
        Export messages by layer.

        This method exports messages from a specified layer in a given format and optionally saves them to a file.

        Args:
            layer_name (str): The name of the layer to export messages from.
            file_format (str): The format to export the messages in. Must be one of the supported formats.
            filepath (str, optional): The path to save the exported messages to. If not provided, the messages will not be saved to a file.
            compress (bool, optional): Whether to compress the exported messages. Defaults to False.

        Returns:
            bytes: The exported messages in the specified format.

        Raises:
            FormatException: If the provided file_format is not supported.
        """
        if file_format not in self._formats: raise FormatException("Invalid format")

        svc = "exchange/export_messages"
        params={"layerName":layer_name,
				"format":file_format,
				"compress":1*compress}
        result = self._engine.request(svc,params,sid=self._engine.auth.get_sid(),file=True)
        if filepath:
            with open(filepath,"wb") as f:
                f.write(result)
        return result
    
    def export_messages_by_id(self,unit_id:int,date_from:datetime,date_to:datetime,file_format:str,filepath:str=None,compress:bool=False):
        """
        Export messages for a specific unit within a given time range.

        Args:
            unit_id (int): The ID of the unit to export messages for.
            date_from (datetime): The start date and time for the export range.
            date_to (datetime): The end date and time for the export range.
            file_format (str): The format of the exported file. Must be one of the supported formats.
            filepath (str, optional): The path to save the exported file. If None, the result is returned without saving to a file. Defaults to None.
            compress (bool, optional): Whether to compress the exported file. Defaults to False.

        Raises:
            FormatException: If the provided file format is not supported.

        Returns:
            bytes: The exported messages in the specified format.
        """
        if file_format not in self._formats: raise FormatException("Invalid format")

        svc = "exchange/export_messages"
        params={"itemId":unit_id,
                "timeFrom":int(datetime.timestamp(date_from)),
                "timeTo":int(datetime.timestamp(date_to)),
                "format":file_format,
                "compress":1*compress}
        result = self._engine.request(svc,params,sid=self._engine.auth.get_sid(),file=True)
        if filepath:
            with open(filepath,"wb") as f:
                f.write(result)
        return result


