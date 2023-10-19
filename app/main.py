
from . import models
from .database import engine
from fastapi import FastAPI
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine) 
#connecting sqlalchemy into the main.py

app = FastAPI() 
#initiating fastapi using api variable

origins = [
    # "https://www.google.com"
    "*" # makes it public 
]
#allows sites that the resources can be shared with 

#code copied from fastapi docs > cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {'message': 'hello'}

app.include_router(post.router) 
app.include_router(user.router) 
app.include_router(auth.router)
app.include_router(vote.router)
# all models are connected through router to the main py compulsarily, explanation in post model