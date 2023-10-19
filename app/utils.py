# here we will store many utilities associated with the main py

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto") #we are using bcrypt scheme to handle password security using cryptcontext

def hash(password: str):
     return pwd_context.hash(password)
   
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)