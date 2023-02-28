from fastapi import FastAPI, Request
#from dbmodel import MainModel
from db import connect_to_mongo
from routes.monica import monicaRouter
from datetime import datetime

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

@app.api_route("/{path_name:path}", methods=["GET"])
async def catch_all(request: Request, path_name: str):
    return {
        "request_method": request.method,
        "path_name": path_name,
        "message": "Hallo! Reply from RAFAEL API at " +
        datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

