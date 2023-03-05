from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.user import User, TokenData, UserInDB
from db import connect_to_mongo
from datetime import datetime, timedelta
from config import Config

c = Config()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_coll = "users"
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
    
async def get_user(db, username: str):
    conn = await connect_to_mongo()
    coll = conn[db]
    user_dict = await coll.find_one({"username": username},{'_id': 0})
    if user_dict:
        return UserInDB(**user_dict)

async def authenticate_user(collection, username: str, password: str):
    conn = await connect_to_mongo()
    coll = conn[collection]
    user = await coll.find_one({"username": username},{'_id': 0})
    if not user:
        return False
    if not verify_password(password, user['hashed_password']):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, c.security_key(), algorithm=c.algorithm())
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, c.security_key(), algorithms=[c.algorithm()])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user("users", username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user