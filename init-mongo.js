var config  = require('.env.dev');

fakeDoc = 
{
  "_id": {
    "$oid": "62162d2f7e191f1599cca03d"
  },
  "Date": {
    "$date": {
      "$numberLong": "1645574400000"
    }
  },
  "ID_AFE": "AirH336",
  "Ver_FMW": "AH_1.3.1",
  "lbl_location": "AirH-Pitch1",
  "location": {
    "coordinates": [
      15.047446452336533,
      37.36084832653023
    ],
    "type": "Point"
  },
  "samples": [
    {
      "data": {
        "CO_WE": 359.407,
        "CO_AE": 259.645,
        "NO2_WE": 306.608,
        "NO2_AE": 294.688,
        "NO2_O3_WE": 424.434,
        "NO2_O3_AE": 404.748,
        "temp": 22.6,
        "hum": 22,
        "PM_Model1": {
          "PM_SP_UG_1_0": 3,
          "PM_SP_UG_2_5": 4,
          "PM_SP_UG_10_0": 4
        },
        "PM_Model2": {
          "PM_AE_UG_1_0": 3,
          "PM_AE_UG_2_5": 4,
          "PM_AE_UG_10_0": 4
        },
        "PM_BINS": {
          "PM_NP_0_3": 660,
          "PM_NP_0_5": 188,
          "PM_NP_1_0": 18,
          "PM_NP_2_5": 0,
          "PM_NP_5_0": 0,
          "PM_NP_10_0": 0
        },
        "CO": 0.475,
        "NO2": 24.234,
        "O3": 67.879,
        "PM10": -4841.62,
        "PM2_5": -5887.18
      },
      "t": {
        "$date": {
          "$numberLong": "1645620526197"
        }
      },
      "PM_DIAG": 0,
      "vAFE": 4288.215,
      "batt": 100
    }
  ]
}

db.createUser(
  {
    user : config.MONGO_USER,
    pwd : config.MONGO_PASSWORD,
    roles : [
      {  
        role : "readWrite",
        db : "rafael"
      }
    ]
  }
)

db.monica.insert(
  fakeDoc
)