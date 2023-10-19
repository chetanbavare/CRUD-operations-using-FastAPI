
from typing import List, Optional
from ..schema import Post
from sqlalchemy.orm import Session
from random import randrange
import time
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response , status


from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor

from ..schema import PostCreate, Post, User, CreateUser, Vote
from .. import models, utils #from current directory
from ..database import engine, get_db# from database file
from ..oauth2 import current_user



router =APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_202_ACCEPTED)
def voted(vote:Vote, current_user : int = Depends(current_user), db:Session = Depends(get_db)):
    
    post_exists = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if not found_vote:
             new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
             db.add(new_vote)
             db.commit()
             return {"message": "Voted Successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"the user with id {current_user.id} has already voted post {vote.post_id}")
        
    if vote.dir == 0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "user hasnt voted this post")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return{"message": "Vote removed successfully"}

    