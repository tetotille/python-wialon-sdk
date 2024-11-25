from datetime import datetime
from .errors import InvalidInput

class Items:
    def __init__(self,engine):
        self._engine = engine
        self._items_type = {
            "hardware":"avl_hw",
            "resource":"avl_resource",
            "retranslator":"avl_retranslator",
            "unit": "avl_unit",
            "unit_group":"avl_unit_group",
            "user": "user",
            "route": "avl_route"
        }
        
    def search(self,id:int=None,item_type:str=None,date_from:datetime=datetime.fromtimestamp(0),date_to:datetime=datetime.fromtimestamp(4294967295),flags:int=0x1,by:str="property",**kwargs):
        svc = "core/search_item"
        if by == "property":
            svc = svc + "s"
            if item_type not in self._items_type.keys(): raise InvalidInput("Please send a valid 'item_type'")
            if (item_type is None): raise Exception("For property you need the 'item_type', 'date_from' and 'date_to' parameters")
            params = {
                "spec": {
                    "itemsType": self._items_type[item_type],
                    "propName": kwargs.get("prop_name","sys_name"),
                    "propValueMask": kwargs.get("prop_mask","*"),
                    "sortType": kwargs.get("sort_by",""),
                    # "propType": kwargs.get("prop_type","property"),
                    # "or_logic": kwargs.get("or_logic",0),
                },
                "force": kwargs.get("force",0),
                "flags": flags,
                "from": int(datetime.timestamp(date_from)),
                "to": int(datetime.timestamp(date_to))
            }
        elif by=="id":
            if id is None: raise Exception("The ID parameter must enter")
            params = {
                "id":id,
                "flags":flags
            }   
            
        else:
            raise Exception("The 'by' or 'property' parameter must be")
        return self._engine.request(svc, params,self._engine.auth.get_sid())    
    