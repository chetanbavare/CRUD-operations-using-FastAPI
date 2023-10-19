
# handles the open authorization of all requests

#following code taken from fast api rdb
from fastapi import Depends, HTTPException, status
import jwt
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

#handles functions needed for authorization

from .database import get_db
from .schema import TokenVerify
from .models import Users
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oath_scheme = OAuth2PasswordBearer(tokenUrl="login") # this method takes the url from which token has been created for verification

def create_access_token(data: dict):
    to_encode = data.copy()  # to keep a backup of data to avoid manipulation
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # orginal time + the time avaliable to use
    print(expiry)
    to_encode.update({"exp":expiry}) # expiry added

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # encode(what to encode, encode with what...)
    return token

def verify_token(token:str,credential_exception): # here the actual work is done of cverification
    try:
        #print(token)
        payload = jwt.decode(token,SECRET_KEY, algorithms=ALGORITHM) # decode the token just like encoding
        id:str = payload.get("user_id")     # obtain id from decoded token
        if id is None:
            raise credential_exception
            #raise HTTPException(status_code=status.HTTP_100_CONTINUE, detail = "id is none error")
        token_data = TokenVerify(id=id)  # verify the id from schema with id obtained from token
    except jwt.PyJWTError:
        raise credential_exception
        #raise HTTPException(status_code=status.HTTP_101_SWITCHING_PROTOCOLS, detail="pyjwt error")
    
    return token_data       # this will return if no exceptions and request will be accepted

def current_user(token:str = Depends(oath_scheme), db:Session = Depends(get_db)): # from post.py , check create_posts function, token str is authorized using oath_scheme variable initialized at the top
    
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="dont know", headers={"WWW-Authenticate" : "Bearer"}) # for not proper authorization
    token = verify_token(token,credential_exception)
    user = db.query(Users).filter(Users.id == token.id).first()
    return user