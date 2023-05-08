from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta

from pydantic import BaseModel
from models import User, UserRole

from passlib.context import CryptContext
from jose import JWTError, jwt

class TokenData(BaseModel):
    username: str

# Создайте секретный ключ для подписи JWT-токенов
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Создайте экземпляр CryptContext для работы с паролями
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Создайте экземпляр OAuth2PasswordBearer для получения токенов доступа
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user(username: str):
    return await User.get(username=username)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, password_hash: str):
    return pwd_context.verify(plain_password, password_hash)

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_admin(current_user: User = Depends(get_current_user)):
    if not current_user.role == UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="Not a superuser")
    return current_user

