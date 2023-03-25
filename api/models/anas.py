from pydantic import BaseModel
from typing import Optional
import datetime 

class DeltaT(BaseModel):
    value: float
    uom: str="s"

class Sample(BaseModel):
    time: datetime.datetime
    rate: DeltaT
    stats: dict
    filename: str
    extension: str
    checksum: str

class Location(BaseModel):
    type: str="Point"
    coordinates: list[float]

class Cabin(BaseModel):
    name: str
    location: Location

class Producer(BaseModel):
    institution: str
    reference: Optional[str] = None
    
class ANASModel(BaseModel):
    date: datetime.datetime
    cabin: Cabin
    producer: Producer
    samples: list[Sample]