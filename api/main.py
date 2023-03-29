from fastapi import FastAPI, Depends
from routes.monica import router as monica_router
from routes.anas import router as anas_router
from routes.auth import router as auth_router
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
app.include_router(anas_router, 
                    dependencies=[Depends(auth_utils.get_current_active_user)]
                )