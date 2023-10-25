from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
      

    # schema are added inside def function , decides what is returned
class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True
    

class PostCreate(PostBase):
    pass

class CreateUser(BaseModel): # schema that will be shown when returned
    id: int
    email:EmailStr
    created_at: datetime
    phone_num: str
    

class Post(PostBase): # used as output schema
    id:int
    # title:str, we will inherit these
    # content:str
    # published: bool
    created_at: datetime # datetime datatype need to import though
    # class Config:
    #     orm_mode= True , this was used to convert sqlalchemy to dict before
    owner_id: int
    owner_of_the_post: CreateUser # will fetch user details related to the post called
    
class PostNew(BaseModel):
    post:Post
    votes:int
    
class User(BaseModel): # actual schema that controls the data inputed
    email : EmailStr
    password: str
    phone_num:str
    

class LoginUser(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    token:str
    token_type:str
    
class TokenVerify(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id : int
    dir : conint(le=1) # this will make sure value added is intger that is less than equal to 1