from fastapi import APIRouter, Depends
from db import connect_to_mongo
from typing import List#, Optional
from datetime import datetime#, tzinfo, timezone
from models.anas import ANASModel



router = APIRouter(
    prefix="/api/anas",
    tags=["ANAS"]
)


collection = 'anas'

@router.get("/one", response_model=ANASModel)
async def getOneDocument():
    '''**Get one document**
        
    - **Returns**:
        - doc: *One single data.*
    '''
    conn = await connect_to_mongo()
    coll = conn[collection]
    result = await coll.find_one({},{'_id': 0})
    return result



@router.get("/dateRange/", response_model=List[ANASModel])
async def getDataByDateRange(
                                    start: str = "2022-02-23", 
                                    end: str = "2022-03-23"
                                ):
    '''**Get all data by date range**
    
    - **Note**: 
        - Remembering that in python the end element is not included in a range:
            - if you want a single day, just insert the day you want as start and the next day as end. *Example: 2020-01-01 and 2020-01-02 to get 2020-01-01 data*.
            - if you want a range of days, insert the first day as start and the day after the last day you want as end. *Example: 2020-01-01 and 2020-01-03 to get 2020-01-01 and 2020-01-02 data*.
        - Insert date as YYYY-MM-DD.
    
    - **Args**:
        - start (str): *start date*. 
        - end (str): *end date*. 
        
    - **Returns**:
        - list: *list of data.*
    '''
    s = datetime.strptime(start, '%Y-%m-%d')
    e = datetime.strptime(end, '%Y-%m-%d')
    conn = await connect_to_mongo()
    coll = conn[collection]
    pipeline = [
        {
            "$match": {
                "date": {
                    "$gte": s,
                    "$lt": e
                }
            }
        }
        ]  
    result = await coll.aggregate(pipeline).to_list(None)
    return result



@router.get("/cabinCount")
async def getCabinCount():
    '''**Get Cabin name and count**
    
    - **Returns**:
        - list: *list of Cabin name and count.*
    '''
    conn = await connect_to_mongo()
    coll = conn[collection]
    pipeline = [
                    {
                        '$group': {
                            '_id': '$cabin.name', 
                            'count': {
                                '$sum': 1
                            }
                        }
                    }
                ]
    result = await coll.aggregate(pipeline).to_list(None)
    return result



# @router.get("/variables", response_model=ANASModel)
# async def getVars():
#     '''**Get one document**
        
#     - **Returns**:
#         - doc: *One single data.*
#     '''
#     conn = await connect_to_mongo()
#     coll = conn[collection]
#     result = await coll.find_one({},{'_id': 0, 'samples.stats'})
#     return result



@router.get("/var/dateRange/")
async def getVarByDateRange(
                                    var: str = "ACC_EX_1", 
                                    start: str = "2022-01-05", 
                                    end: str = "2022-01-06"
                                ):
    '''**Get mean and std values for selected variable by date range**
    
    - **Note**: 
        - Remembering that in python the end element is not included in a range:
            - if you want a single day, just insert the day you want as start and the next day as end. *Example: 2020-01-01 and 2020-01-02 to get 2020-01-01 data*.
            - if you want a range of days, insert the first day as start and the day after the last day you want as end. *Example: 2020-01-01 and 2020-01-03 to get 2020-01-01 and 2020-01-02 data*.
        - Insert date as YYYY-MM-DD.
    
    - **Args**:
        - var (str): *variable name*. 
        - start (str): *start date*. 
        - end (str): *end date*. 
        
    - **Returns**:
        - list: *list of data.*
    '''
    s = datetime.strptime(start, '%Y-%m-%d')
    e = datetime.strptime(end, '%Y-%m-%d')
    conn = await connect_to_mongo()
    coll = conn[collection]
    pipeline = [
    {
        '$match': {
            'date': {
                '$gte': s, 
                '$lt': e
            }
        }
    }, {
        '$project': {
            'date': 1, 
            'meanValues': '$samples.stats.'+var+'.mean', 
            'stdValues': '$samples.stats.'+var+'.std'
        }
    }, {
        '$group': {
            '_id': 0, 
            'date': {
                '$addToSet': '$date'
            }, 
            'meanVaules': {
                '$addToSet': '$meanValues'
            }, 
            'stdVaules': {
                '$addToSet': '$stdValues'
            }
        }
    }
]  
    result = await coll.aggregate(pipeline).to_list(None)
    return result


