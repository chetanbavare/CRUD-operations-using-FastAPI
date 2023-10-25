
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, logger, status
from ..schema import User, CreateUser
from .. import models, utils #from current directory
from ..database import get_db# from database file
from .. import oauth2

router = APIRouter(
    prefix = "/users",
    tags=["Users"]  # explanation in post model
    ) # prefix is used to avoid repetition of path ex. users/id , users/ same done for post model
                                


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CreateUser)
def create_user(user:User, db:Session = Depends(get_db)): # user is schema 
    
    
        hashed = utils.hash(user.password) # this will store the password as random string
        print(user.password)
        print(hashed)
        user.password = hashed
        new_user = models.Users(**user.model_dump()) # Users is models
        # new_user = models.Users(email = user.email, password = user.password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    



@router.get("/{id}", response_model=CreateUser) 
def get_user(id : int, db:Session = Depends(get_db)):
    get_query = db.query(models.Users).filter(models.Users.id == id).first()

    if not get_query:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    
    return get_query

@router.get("/", response_model=List[CreateUser])
def get_all_users(db:Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users

