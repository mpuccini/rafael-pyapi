from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth import get_current_active_user, fake_users_db, fake_hash_password, UserInDB
from models.user import User

authRouter = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# def fake_decode_token(token):
#     return User(
#         username=token + "fakedecoded", email="john@example.com", full_name="John Doe", organization="Enea", disabled=False
#     )


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     return user


@authRouter.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@authRouter.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user