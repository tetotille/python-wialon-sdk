from datetime import datetime

from typing import Any,Optional

class Messages:
    def __init__(self, engine:Any):
        self._engine = engine
        self._unit_messages = {
            "data": 0x0,
            "SMS": 0x100,
            "command": 0x200,
            "event": 0x600,
            "video_usage": 0x2000
        }
        self._resource_messages = {
            "default": 0x0,
            "notification": 0x300,
            "billing_message": 0x500,
            "SMS_for_driver": 0x900
        }
        self._message_filter = {
            "position": 0x1,
            "input": 0x2,
            "output": 0x4,
            "state": 0x8,
            "alarm_bit": 0x10,
            "avl_driver": 0x20,
            "lbs_corrected": 0x20000,
            "wifi_position": 0x80000
        }
        self._event_filter = {
            "violation": 0x1,
            "maitenance": 0x2,
            "route_control": 0x4,
            "maitenance_registered":0x10,
            "filling_registered":0x20
        }
        
        self._logs = 0x1000
        
    def load_interval(self,
                      item_id:int,
                      time_from:datetime=datetime.fromtimestamp(0),
                      time_to:datetime=datetime.fromtimestamp(4294967295),
                      **kwargs:Any):
        """
        Load messages for a certain interval.

        Parameters
        ----------
        item_id : int 
            The ID of the item to load messages for.
        time_from : datetime
            The start time of the interval.
        time_to : datetime 
            The end time of the interval.
        message_type : {'data','SMS','command','event','video_usage'}, default 'data'
            The type of messages to load.
        resource : {'default','notification','billing_message','SMS_for_driver'}, default 'default'
            The resource to load messages from.
        log : bool, optional, default False
            Whether to include logs.
        message_filter : {None,'position','input','output','state','alarm_bit','avl_driver','lbs_corrected','wifi_position'}, optional
            The filter to apply to messages:
            
            * position: position information is available
            * input: input data information is available
            * output: output data information is available
            * state: state information is available
            * alarm_bit: message contains alarm bit
            * avl_driver: message contains information about driver code which come only in parameter avl_driver
            * lbs_corrected: message was corrected by lbs
            * wifi_position: message contains wi-fi position
            
        event_filter : {None,'violation','maitenance','route_control','maitenance_registered','filling_registered'}, optional
            The filter to apply to events:
            
            * violation: violation
            * maitenance: maintenance event
            * route_control: route control event
            * maitenance_registered: is set in addition to flag 0x2: maintenance is registered
            * filling_registered: is set in addition to flag 0x2: registered filling
            
        mask_filter : str, optional
            The mask filter to apply.
        flags_mask : int, optional
            The flags mask. Defaults to 0xff00.
        load_count : int, optional
            The number of messages to load. Defaults to 0xffffffff.

        Returns
        -------
        dict
            The response from the engine request.
            
        Raises
        ------
        InvalidInput
            Failed to get the current user.
        UnknownError
            Failed to fetch messages for the interval.
        AccessDenied
            Failed to fetch the message manager.
        EncodingError
            Accept-encoding is not gzip.
        """
        
        mtype = self._unit_messages[kwargs.get("message_type","data")]
        resource = self._resource_messages[kwargs.get("resource","default")]
        log = self._logs if kwargs.get("log",False) else 0
        message_filter = self._process_filter(kwargs.get("message_filter",None),kwargs.get("event_filter",None),kwargs.get("mask_filter"))
        svc = "messages/load_interval"
        params = {
            "itemId": item_id,
            "timeFrom": int(datetime.timestamp(time_from)),
            "timeTo": int(datetime.timestamp(time_to)),
            "flags": mtype | resource | log | message_filter,
            "flagsMask": kwargs.get("flags_mask",0xff00),
            "loadCount": kwargs.get("load_count",0xffffffff),
        }
        for key in list(params):
            if params[key] is None:
                del params[key]

        return self._engine.request(svc, params,self._engine.auth.get_sid())["messages"]

    def load_last(self,item_id:int,last_time:int,last_count:int,flags:Optional[int],flags_mask:Optional[int],load_count:Optional[int]):
        """
        To load a few latest messages for a specified point in time.
        Args:
            item_id (int): The ID of the item to load messages for.
            last_time (int): The timestamp of the last message to load.
            last_count (int): The number of last messages to load.
            flags (int): The flags to filter messages.
            flags_mask (int): The mask to apply to the flags.
            load_count (int): The number of messages to load.
        Returns:
            dict: The response from the Wialon server containing the loaded messages.  
        
        ## Errors:
            7: Failed to fetch the message manager with the required ACL (ADF_ACL_ITEM_EXECUTE_REPORTS).
            6: Failed to fetch unit messages.
            4: No messages found for the specified interval, or the number of messages exceeds the limit (10000).
        """
        
        svc = "messages/load_last"
        params = {
            "itemId": item_id,
            "lastTime": last_time,
            "lastCount": last_count,
            "flags": flags,
            "flagsMask": flags_mask,
            "loadCount": load_count,
        }
        for key in list(params):
            if params[key] is None:
                del params[key]
    
        return self._engine.request(svc, params,self._engine.auth.get_sid())

    def _process_filter(self,message:str,event:str,mask:Optional[int]) -> int:
        # TODO: create mask filter
        message_filter = 0
        if message:
            for m in message.split(','):
                m = m.strip()
                if m in self._message_filter:
                    message_filter |= self._message_filter[m]
        
        event_filter = 0
        if event:
            for e in event.split(','):
                e = e.strip()
                if e in self._event_filter:
                    event_filter |= self._event_filter[e]
        
        mask_filter = mask if mask is not None else 0
        
        return message_filter | event_filter | mask_filter