from fastapi import FastAPI, Request, Depends
#from dbmodel import MainModel
#from db import connect_to_mongo
from routes.monica import router as monica_router
from routes.auth import router as auth_router
#from datetime import datetime
import auth_utils

app = FastAPI(
    title="RAFAEL API",
    description="RESTful API for RAFAEL project",
    version="0.3.1",
    terms_of_service="",
    contact={
        "name": "RAFAEL API info",
        "url": "https://github.com/mpuccini/rafael-pyapi/",
        "email": "marco.puccini@enea.it",
    },
    license_info={"name": "MIT", "url": "https://mit-license.org/"},
)




# actualy add routes
app.include_router(auth_router)
app.include_router(monica_router, 
                    dependencies=[Depends(auth_utils.get_current_active_user)]
                )
