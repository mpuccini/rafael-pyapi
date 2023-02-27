import datetime
from pydantic import BaseModel


class LocationModel(BaseModel):
    type: str
    coordinates: list[float]

class ProducerModel(BaseModel):
    institution: str
    reference: str

class ChannelModel(BaseModel):
    id: str
    name: str
    unit: str

class SamplingModel(BaseModel):
    rate: float
    unit: str

class SensorModel(BaseModel):
    id: str
    type: str
    model: str
    sampling: SamplingModel
    channels: list[ChannelModel]
    producer: ProducerModel
    location: LocationModel
    
class DataModel(BaseModel):
    day: datetime.date
    sensor: SensorModel

class MainModel(BaseModel):
    t: datetime.datetime
    filename: str
    checksum: str
    data: DataModel
    
print(MainModel.schema_json(indent=2))