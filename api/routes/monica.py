from fastapi import APIRouter
from db import connect_to_mongo
from typing import List
from datetime import datetime, tzinfo, timezone
from models.monica import MonicaModel

monicaRouter = APIRouter()
collection = 'monica'

@monicaRouter.get("/one", response_model=MonicaModel)
async def getOneSensor():
    '''**Get one sensor**
        
    - **Returns**:
        - doc: *One single sensor data.*
    '''
    conn = await connect_to_mongo()
    coll = conn[collection]
    result = await coll.find_one({},{'_id': 0})
    return result

@monicaRouter.get("/all", response_model=List[MonicaModel])
async def getAllSensors():
    '''**Get all sensors**
        
    - **Returns**:
        - list: *list of sensors.*
    '''
    conn = await connect_to_mongo()
    coll = conn[collection]
    result = await coll.find({},{'_id': 0}).limit(10).to_list(None)
    return result



@monicaRouter.get("/all/{start_date}:{end_date}", response_model=List[MonicaModel])
async def getAllSensorsByDateRange(start_date: str, end_date: str):
    '''**Get all sensors by date range**
    
    - **Note**: 
        - Remembering that in python the end element is not included in a range:
            - if you want a single day, just insert the day you want as start and the next day as end. *Example: 2020-01-01 and 2020-01-02 to get 2020-01-01 data*.
            - if you want a range of days, insert the first day as start and the day after the last day you want as end. *Example: 2020-01-01 and 2020-01-03 to get 2020-01-01 and 2020-01-02 data*.
        - Insert date as YYYY-MM-DD.
    
    - **Args**:
        - start_date (str): *start date*. 
        - end_date (str): *end date*. 
        
    - **Returns**:
        - list: *list of sensors.*
    '''
    sd = datetime.strptime(start_date, '%Y-%m-%d')
    ed = datetime.strptime(end_date, '%Y-%m-%d')
    conn = await connect_to_mongo()
    coll = conn[collection]
    pipeline = [
        {
            "$match": {
                "Date": {
                    "$gte": sd,
                    "$lt": ed
                }
            }
        }
        ]  
    result = await coll.aggregate(pipeline).to_list(None)
    return result



@monicaRouter.get("/sensorIDcount")
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



@monicaRouter.get("/{sensor_id}")
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



