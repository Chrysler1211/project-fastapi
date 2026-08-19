

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from . import schemas,models
from .database import get_db
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .config import settings


oauth2 = OAuth2PasswordBearer(
    tokenUrl="Login"
)

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_token(data: dict):

    to_encode = data.copy()

    Expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": Expire})

    token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])

        id : str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_info = schemas.token(id=id)

    except InvalidTokenError:
        raise credentials_exception
        
    return token_info



def get_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        headers={"WWW-authenticate": "Bearer"}, detail="Invalid Token")

    token = verify(token, credentials_exception)

    users = db.query(models.Account).filter(models.Account.id == token.id).first()

    return users



