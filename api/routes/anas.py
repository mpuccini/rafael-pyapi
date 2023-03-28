from fastapi import APIRouter#, Depends
from db import connect_to_mongo
from typing import List#, Optional
from datetime import datetime
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


@router.get("/accSTATS/dateRange/")
async def getAccStatsByDateRange(
                                    acc: str = "ACC_AZ_5", 
                                    val: str = "rmsMax",
                                    start: str = "2022-01-05", 
                                    end: str = "2022-01-06"
                                ):
    '''**Get RMS max or max values for selected accelerometer by date range**
    
    - **Note**: 
        - Remembering that in python the end element is not included in a range:
            - if you want a single day, just insert the day you want as start and the next day as end. *Example: 2020-01-01 and 2020-01-02 to get 2020-01-01 data*.
            - if you want a range of days, insert the first day as start and the day after the last day you want as end. *Example: 2020-01-01 and 2020-01-03 to get 2020-01-01 and 2020-01-02 data*.
        - Insert date as YYYY-MM-DD.
    
    - **Args**:
        - acc (str): *accelerometer channel name*. Available Channels: ACC_AZ_5, ACC_EX_1, ACC_EY_2, ACC_EZ_3, ACC_FX_1, ACC_FY_2, ACC_FX_3, ACC_GZ_1, ACC_GZ_2
        - val (str): *Stats value to be returned*. Available values: rmsMax, max
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
            'Values': '$samples.stats.accSTATS.' + val + '.' + acc
        }
    }, {
        '$group': {
            '_id': 0, 
            'date': {
                '$addToSet': '$date'
            }, 
            'Vaules': {
                '$addToSet': '$Values'
            }
        }
    }
]  
    result = await coll.aggregate(pipeline).to_list(None)
    return result


@router.get("/inclSTATS/dateRange/")
async def getInclStatsByDateRange(
                                    incl: str = "incl_D1", 
                                    val: str = "rmsMax",
                                    start: str = "2022-01-05", 
                                    end: str = "2022-01-06"
                                ):
    '''**Get RMS max, min or max values for selected inclinometer by date range**
    
    - **Note**: 
        - Remembering that in python the end element is not included in a range:
            - if you want a single day, just insert the day you want as start and the next day as end. *Example: 2020-01-01 and 2020-01-02 to get 2020-01-01 data*.
            - if you want a range of days, insert the first day as start and the day after the last day you want as end. *Example: 2020-01-01 and 2020-01-03 to get 2020-01-01 and 2020-01-02 data*.
        - Insert date as YYYY-MM-DD.
    
    - **Args**:
        - incl (str): *Inclinometer channel name*. Available Channels: incl_D1, incl_D2
        - val (str): *Stats value to be returned*. Available values: rmsMax, max, min
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
            'Values': '$samples.stats.inclSTATS.' + val + '.' + incl
        }
    }, {
        '$group': {
            '_id': 0, 
            'date': {
                '$addToSet': '$date'
            }, 
            'Vaules': {
                '$addToSet': '$Values'
            }
        }
    }
]  
    result = await coll.aggregate(pipeline).to_list(None)
    return result


@router.get("/strainSTATS/dateRange/")
async def getStrainStatsByDateRange(
                                    strain: str = "STRAIN_A2", 
                                    val: str = "mean",
                                    start: str = "2022-01-05", 
                                    end: str = "2022-01-06"
                                ):
    '''**Get max, min or mean values for selected strain gauge by date range**
    
    - **Note**: 
        - Remembering that in python the end element is not included in a range:
            - if you want a single day, just insert the day you want as start and the next day as end. *Example: 2020-01-01 and 2020-01-02 to get 2020-01-01 data*.
            - if you want a range of days, insert the first day as start and the day after the last day you want as end. *Example: 2020-01-01 and 2020-01-03 to get 2020-01-01 and 2020-01-02 data*.
        - Insert date as YYYY-MM-DD.
    
    - **Args**:
        - incl (str): *Strain gauge channel name*. Available Channels: STRAIN_A2, STRAIN_A3, STRAIN_B3, STRAIN_B4, STRAIN_C3, STRAIN_C4
        - val (str): *Stats value to be returned*. Available values: mean, max, min
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
            'Values': '$samples.stats.strainSTATS.' + val + '.' + strain
        }
    }, {
        '$group': {
            '_id': 0, 
            'date': {
                '$addToSet': '$date'
            }, 
            'Vaules': {
                '$addToSet': '$Values'
            }
        }
    }
]  
    result = await coll.aggregate(pipeline).to_list(None)
    return result

@router.get("/allFilesByDate/")
async def getAllFilesByDate( 
                                    date: str = "2022-01-05"
                                ):
    '''**Get all files checksum for selected date**
    
    - **Args**:
        - date (str): *date*. 
        
    - **Returns**:
        - list: *list of checsums.*
    '''
    date = datetime.strptime(date, '%Y-%m-%d')

    conn = await connect_to_mongo()
    coll = conn[collection]
    pipeline = [
        {
            '$match': {
                'date': date
            }
        }, {
            '$project': {
                '_id': 0,
                'date': 1, 
                'files': '$samples.checksum'
            }
        }
    ]   

    result = await coll.aggregate(pipeline).to_list(None)
    return result