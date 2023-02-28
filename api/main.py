from fastapi import FastAPI
#from dbmodel import MainModel
from db import connect_to_mongo
from routes.monica import monicaRouter

app = FastAPI(
    title="RAFAEL API",
    description="RESTful API for RAFAEL project",
    version="0.1.0",
    terms_of_service="",
    contact={
        "name": "RAFAEL API info",
        "url": "https://github.com/mpuccini/rafael-pyapi/",
        "email": "marco.puccini@enea.it",
    },
    license_info={"name": "MIT", "url": "https://mit-license.org/"},
)
# actualy add routes
app.include_router(monicaRouter, prefix="/api/v1/monica", tags=["Monica"])

