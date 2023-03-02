from fastapi import APIRouter, Depends
from db import connect_to_mongo
from typing import List#, Optional
from datetime import datetime#, tzinfo, timezone
from models.monica import MonicaModel



router = APIRouter(
    prefix="/api/v1/monica",
    tags=["Monica"]
)


collection = 'monica'

@router.get("/one", response_model=MonicaModel)
async def getOneSensor():
    '''**Get one sensor**
        
    - **Returns**:
        - doc: *One single sensor data.*
    '''
    conn = await connect_to_mongo()
    coll = conn[collection]
    result = await coll.find_one({},{'_id': 0})
    return result



@router.get("/dateRange/", response_model=List[MonicaModel])
async def getAllSensorsByDateRange(
                                    start: str = "2022-02-23", 
                                    end: str = "2022-03-23"
                                ):
    '''**Get all sensors by date range**
    
    - **Note**: 
        - Remembering that in python the end element is not included in a range:
            - if you want a single day, just insert the day you want as start and the next day as end. *Example: 2020-01-01 and 2020-01-02 to get 2020-01-01 data*.
            - if you want a range of days, insert the first day as start and the day after the last day you want as end. *Example: 2020-01-01 and 2020-01-03 to get 2020-01-01 and 2020-01-02 data*.
        - Insert date as YYYY-MM-DD.
    
    - **Args**:
        - start (str): *start date*. 
        - end (str): *end date*. 
        
    - **Returns**:
        - list: *list of sensors.*
    '''
    s = datetime.strptime(start, '%Y-%m-%d')
    e = datetime.strptime(end, '%Y-%m-%d')
    conn = await connect_to_mongo()
    coll = conn[collection]
    pipeline = [
        {
            "$match": {
                "Date": {
                    "$gte": s,
                    "$lt": e
                }
            }
        }
        ]  
    result = await coll.aggregate(pipeline).to_list(None)
    return result



@router.get("/sensorIDcount")
async def getSensorIDCount():
    '''**Get sensor IDs and count**
    
    - **Returns**:
        - list: *list of sensors IDs and count.*
    '''
    conn = await connect_to_mongo()
    coll = conn[collection]
    pipeline = [
                    {
                        '$group': {
                            '_id': '$ID_AFE', 
                            'count': {
                                '$sum': 1
                            }
                        }
                    }
                ]
    result = await coll.aggregate(pipeline).to_list(None)
    return result



@router.get("/{sensor_id}")
async def getSensorsByID(sensor_id: str):
    '''**Get sensor by ID**
    
    - **Args**:
        - sensor_id (str): *sensor ID.*
        
    - **Returns**:
        - list: *list of sensors.*
    '''
    conn = await connect_to_mongo()
    coll = conn[collection]
    result = await coll.find({"ID_AFE": sensor_id}, {'_id': 0}).limit(5).to_list(None)
    return result



@router.get("/getMainData/")
async def getMainData(
    start: str = "2022-02-23",
    end: str = "2022-03-23",
):
    '''**Get sensor Main data by Time Range**
    
    - **Note**: get only the main data for all sensors in the time range. In particular, it returns:
        - "temp": temperature in °C
        - "hum": humidity in %
        - "CO": Carbon Monoxide in ppm
        - "NO2": Nitrogen Dioxide in ppm
        - "O3": Ozone in ppm
        - "PM10": Particulate Matter 10 in µg/m3
        - "PM2_5": Particulate Matter 2.5 in µg/m3
        - "t": date and time of the sample
    
    - **Args**:
        - start (str): *start date*.
        - end (str): *end date*.
    
    - **Returns**:
        - list: *list of sensors IDs and count.*
    '''
    s = datetime.strptime(start, '%Y-%m-%d')
    e = datetime.strptime(end, '%Y-%m-%d')
    conn = await connect_to_mongo()
    coll = conn[collection]
    pipeline = [
    {
        '$match': {
            'Date': {
                '$gte': s, 
                '$lt': e
            }
        }
    }, {
        '$project': {
            'Date': 1, 
            'ID_AFE': 1, 
            'samples.t': 1, 
            'samples.data.temp': 1, 
            'samples.data.hum': 1, 
            'samples.data.CO': 1, 
            'samples.data.NO2': 1, 
            'samples.data.O3': 1, 
            'samples.data.PM10': 1, 
            'samples.data.PM2_5': 1
        }
    }, {
        '$group': {
            '_id': None, 
            'dates': {
                '$addToSet': '$Date'
            }, 
            'mainData': {
                '$addToSet': '$samples'
            }
        }
    }
]
    result = await coll.aggregate(pipeline).to_list(None)
    return result

