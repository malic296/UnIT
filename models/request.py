from dataclasses import dataclass

@dataclass
class Request:
    maps: bool = False
    hotspots: bool = False
    vegetation: bool = False
    corelation: bool = False