from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User, UserInDB
from auth_utils import fake_hash_password, get_current_active_user
from db import connect_to_mongo




router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"]
)



@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#    user_dict = fake_users_db.get(form_data.username)
    conn = await connect_to_mongo()
    coll = conn['users']
    user_dict = await coll.find_one({"username": form_data.username},{'_id': 0})
    if not user_dict:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    print(user_dict)
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user