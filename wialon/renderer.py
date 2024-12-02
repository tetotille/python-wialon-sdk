from datetime import datetime
from .errors import InvalidInput

class Render:
    def __init__(self,engine):
        self._engine = engine

    def create_message_layer(self,item_id:int,
                            
                             date_from:datetime,
                             date_to:datetime,
                             trip_detector:bool=False,
                             track_color="cc0000ff",
                             track_width:int=4,
                             arrows:bool=True,
                             points:bool=True,
                             point_color="cc0000ff",
                             annotations:bool=False,
                             **kwargs):
        """Creates a message layer for a given item within a specified time range.
        Args:
            item_id (int): The ID of the item for which the message layer is created.
            date_from (datetime): The start date and time for the message layer.
            date_to (datetime): The end date and time for the message layer.
            trip_detector (bool, optional): Whether to use the trip detector. Defaults to False.
            track_color (str, optional): The color of the track in hexadecimal format. Defaults to "cc0000ff".
            track_width (int, optional): The width of the track. Defaults to 4.
            arrows (bool, optional): Whether to display arrows on the track. Defaults to True.
            points (bool, optional): Whether to display points on the track. Defaults to True.
            point_color (str, optional): The color of the points in hexadecimal format. Defaults to "cc0000ff".
            annotations (bool, optional): Whether to display annotations. Defaults to False.
            **kwargs: Additional optional parameters for customizing the message layer.
        Keyword Args:
            grouping_markers (bool, optional): Whether to group markers. Defaults to False.
            numbering_for_markers (bool, optional): Whether to number markers. Defaults to False.
            events_markers (bool, optional): Whether to display event markers. Defaults to False.
            fillings (bool, optional): Whether to display fillings. Defaults to False.
            images (bool, optional): Whether to display images. Defaults to False.
            parkings (bool, optional): Whether to display parkings. Defaults to False.
            speedings (bool, optional): Whether to display speedings. Defaults to False.
            stops (bool, optional): Whether to display stops. Defaults to False.
            thefts (bool, optional): Whether to display thefts. Defaults to False.
            video_markers (bool, optional): Whether to display video markers. Defaults to False.
        Returns:
            dict: The response from the engine request.
        Raises:
            NoMessagesForSelectedInterval: If there are no messages for the selected interval.
        """
        name = "messages"
        svc = "render/create_messages_layer"
        group_marker = kwargs.get("grouping_markers",False)
        number_marker = kwargs.get("numbering_for_markers",False)
        event_marker = kwargs.get("events_markers",False)
        fillings = kwargs.get("fillings",False)
        images = kwargs.get("images",False)
        parkings = kwargs.get("parkings",False)
        speedings = kwargs.get("speedings",False)
        stops = kwargs.get("stops",False)
        thefts = kwargs.get("thefts",False)
        video_markers = kwargs.get("video_markers",False)
        flags = 0x1*group_marker | 0x2*number_marker | 0x4*event_marker | 0x8*fillings | 0x10*images | 0x20*parkings | 0x40*speedings | 0x80*stops | 0x100*thefts | 0x200*video_markers
        params = {"layerName":"messages",
					 "itemId":item_id,
					 "timeFrom":int(date_from.timestamp()),
					 "timeTo":int(date_to.timestamp()),
					 "tripDetector":trip_detector,
					 "trackColor":track_color,
					 "trackWidth":track_width,
					 "arrows":arrows,
					 "points":points,
					 "pointColor":point_color,
					 "annotations":annotations,
					 "flags":flags}
        return self._engine.request(svc=svc,params=params,sid=self._engine.auth.get_sid())

    def remove_layer(self,name:str):
        """
        Remove a layer from the Wialon map.

        Args:
            name (str): The name of the layer to be removed.

        Returns:
            bool: True if the layer was successfully removed, False if there was an InvalidInput exception.
        """
        svc = "render/remove_layer"
        params = {"layerName": name}
        try:
            self._engine.request(svc=svc,params=params,sid=self._engine.auth.get_sid())
        except InvalidInput:
            return False
        return True
