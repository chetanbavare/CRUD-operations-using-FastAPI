
#authorization requests are handled here

from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..schema import LoginUser
from ..database import get_db
from ..models import Users
from .. import utils
from ..import oauth2



router = APIRouter(tags=["Authentication"])



@router.post("/login")
# we are not using schema to get the input , which is in body json, instead we are using oauth2passwordrequestform to accept input as form data which is username and password 
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),  db:Session = Depends(get_db)):
# def login(user_credentials: LoginUser,  db:Session = Depends(get_db)):
    # user = db.query(Users).filter(Users.email == user_credentials.email).first() 
    user = db.query(Users).filter(Users.email == user_credentials.username).first() # input is not email anymore, new import expects username and password (username can be a email though)
    # print(user.email)
    # print(user.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid email")
    
    # if not utils.verify(user_credentials.password, user.password):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid password")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid password")
    
    # if user_credentials.password != user.password:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid password")
    
    user_token = oauth2.create_access_token({"user_id" : user.id}) # what column to encode, expecting a dict object, as JWT only supports JSON objects as payloads, hence need to give a key value pair


    return {"token" : user_token, "token_type" : "bearer"}

