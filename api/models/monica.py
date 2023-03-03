import datetime
from pydantic import BaseModel
from typing import List

class LocationModel(BaseModel):
    type: str
    coordinates: list[float]

class PM_Model1(BaseModel):
    PM_SP_UG_1_0: int
    PM_SP_UG_2_5: int
    PM_SP_UG_10_0: int
    
class PM_Model2(BaseModel):
    PM_AE_UG_1_0: int
    PM_AE_UG_2_5: int
    PM_AE_UG_10_0: int
    
class PM_BINS(BaseModel):
    PM_NP_0_3: int
    PM_NP_0_5: int
    PM_NP_1_0: int
    PM_NP_2_5: int
    PM_NP_5_0: int
    PM_NP_10_0: int

class Data(BaseModel):
    CO_WE: float
    CO_AE: float
    NO2_WE: float
    NO2_AE: float
    NO2_O3_WE: float
    NO2_O3_AE: float
    temp: float
    hum: float
    PM_Model1: PM_Model1
    PM_Model2: PM_Model2
    PM_BINS: PM_BINS
    CO: float
    NO2: float
    PM10: float
    PM2_5: float


class DataModel(BaseModel):
    data: Data
    t: datetime.datetime
    PM_DIAG: int
    vAFE: float
    batt: int

class MonicaModel(BaseModel):
    _id: str
    Date: datetime.date
    ID_AFE: str
    Ver_FMW: str
    lbl_location: str
    location: LocationModel
    samples: list[DataModel]
    
class MainDataModel(BaseModel):
    temp: float
    hum: float
    CO: float
    NO2: float
    O3: float
    PM10: float
    PM2_5: float
    
class MainSampleModel(BaseModel):
    t: datetime.datetime
    data: MainDataModel
    
class ResponseMainModel(BaseModel):
    Dates: list[datetime.date]
    # ID_AFE: str
    Samples: list[list[MainSampleModel]]