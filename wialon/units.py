from typing import Dict, Union, Any

class Unit:
    def __init__(self,data:Dict[str,Union[int,str]]):
        self._measure_units = ["System International","United States", "Imperial", "Metric with Gallons"]
        self._data = data
        self.measure_unit:str = self._measure_units[int(data["mu"])]
        self.name = data["nm"]
        self.cls = "unit" # Superclass ID
        self.id = self._data["id"]
        
    def __str__(self):
        data = f"Name: {self.name}\nid: {self.id}\nUnitType: {self.cls}"
        return data
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Unit):
            return self.id == other.id
        return False
        

class Units:
    def __init__(self, engine: Any):
        self._engine = engine
        
    