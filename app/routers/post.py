
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from random import randrange
import time
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response , status


from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor

from ..schema import PostCreate, Post, User, CreateUser, PostNew
from .. import models, utils #from current directory
from ..database import engine, get_db# from database file
from ..oauth2 import current_user

router = APIRouter(
    prefix="/posts", # exp in user model
    tags = ["Post"] # this will group all the post model http requests under one section in swagger ui ie 127.0.0.1:8000/docs
    ) # we will be importing apirouter and store in router and it will be called in main py through app

@router.get("/", response_model= List[PostNew]) # list[post] needs to be used here as we are fetching more than one posts
# now we are using new schema which holds two ids post(which further contains the regular ids) and vote
# @router.get("/") # list[post] needs to be used here as we are fetching more than one posts
def test_posts(db: Session = Depends(get_db), current_user : int = Depends(current_user) , Limit:int = 30, skip:int = 0, search : Optional[str] = ""):
    # limit is a key that handles no of results in a query ,here max is 10 ex. ?limit = 3 
    # skip to skip over some results 
    # for search , we are using optional i.e it either has str or nothing, ex. search = ayush%20added , %20 is speacial cahacter for space
    #use & to seperate two key parameters : skip= 2 &limit = 3

    #cursor.execute("select * from posts") # used to define queries
    #posts = cursor.fetchall(); # used to execute defined queries, fetchall for checking all rows, fetchone for returning first row satisfying the query
    #return my_posts
    # print(Limit)
    # print(skip)
    # print(search)
    # print(models.Post.title.contains(search)) 

    posts = db.query(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all() # this is same as select * from posts where user.id = post.owner_id
  
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip)
    #this is the same as select posts.*, count(votes.post_id) from posts left join votes on posts.id = votes.post_id group by posts.id
    # without .all() this is just a query waiting to be executed
    print(results)
    return [{"post": result[0], "votes": result[1]} for result in results] 

# for result in results: This is a list comprehension that iterates over each element (result) in the results list.
# {"post": result[0], "votes": result[1]}: For each result, this creates a new dictionary. The dictionary has two key-value pairs:
# "post": result[0]: This assigns the first element (result[0]) of the result list to the key "post".
# "votes": result[1]: This assigns the second element (result[1]) of the result list to the key "votes".
# This means that for each result in the list, you're creating a dictionary with two keys: "post" and "votes", where "post" holds the first element of the result list and "votes" holds the second element.
# The list comprehension creates a list of these dictionaries for each result in results.
# Finally, you're returning this list of dictionaries.
# In your specific case, results likely contains rows from your database query where each row has two elements: the post information and the count of votes. By creating dictionaries with specific keys ("post" and "votes") for each row, you're structuring the data in a way that can be easily processed and returned by your FastAPI application.

    # return results

@router.get("/{id}") #id is now a string 
# @router.get("/{id}", response_model=PostNew) #id is now a string 
def get_post(id:int, db:Session = Depends(get_db), current_user : int = Depends(current_user)): # made int for validation 
    #post=find_post(id) 
    #print(id)
    
    #cursor.execute("select * from posts where id = %s", (str(id))) # back to string because query is a string 
    #get_post_by_id=cursor.fetchone();
    #print(get_post_by_id)

    get_post_by_id = db.query(models.Post).filter(models.Post.id == id).first() # filter acts as where , first used to avoid iteration of whole table 
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)

    if not get_post_by_id:
       raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} wasnt found")

    if get_post_by_id.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="not authorize to update this post")
    
    # return get_post_by_id
    return  [{"post": result[0], "votes": result[1]} for result in results] 
    # return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post) # response model is used to return data respective to the Post schema (excluding columns that arent present) this is a pydantic model example
def create_posts(post: PostCreate, db:Session=Depends(get_db),  current_user : int = Depends(current_user)): # current_user handles the authentication , current_user is a function from oath2
    # the above post:PostCreate is the input schema
    #response_model is the output schema, that will be returned in postman
    #post_dict = post.model_dump()
    #post_dict['id'] = randrange(0,1000000)
    #my_posts.append(post_dict)
    
    #using psycopg2 driver and its cursor object

    #cursor.execute("""Insert into posts (title,content) values(%s, %s) returning * """ , (post.title, post.content))
    # always use parameterized variables %s for input ,as using f string like f'{post.title} may lead to sql injection 
    #new_post = cursor.fetchone()
    #conn.commit() # used to commit changes created in database

    #using sqlalchemy for inbuilt python objects to run sql query
    #new_post = models.Post(title = post.title, content = post.content, published=post.published) this is for less columns
    # if two many columns use dictionary
    print(current_user.email) # this is returning the object user from function in oauth2 py
    print(current_user.id) # we will add this in the next line to automatically get the id of user that has logged in and add it as owner_id
    new_post = models.Post(owner_id = current_user.id, **post.model_dump()) # schema to dictionary and then unpacked into the model using **
    db.add(new_post) # to add newly added row
    db.commit() # commit
    db.refresh(new_post) # for returning *

    return new_post # this returns a sqlalchemy model but converted to a valid dict for pydantic model in new update

@router.put("/{id}", response_model=Post,status_code=status.HTTP_403_FORBIDDEN)
def update_post(id:int, updated_post:PostCreate, db:Session = Depends(get_db), current_user : int = Depends(current_user)):
    #index = find_index_post(id) # for id = 1 , index = 0

    #cursor.execute('update posts set title = %s , content = %s, published = %s where id = %s returning *',(post.title, post.content, post.published,str(id)) )
    #updated_post = cursor.fetchone();
    #conn.commit();

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} not found ')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="not authorize to update this post")
    
    #post_query.update({
    #                    "title":"hey this is updated data", 
    #                   "content":"this is my updated content"
    #                  }, synchronize_session = False)
    # for user input :

    post_query.update(updated_post.model_dump(), synchronize_session=False) # schema converted to dictionary accepts json notation

    #post_dict = post.model_dump()
    #post_dict['id'] = id # so give id value as 1
    #my_posts[index] = post_dict # and post the values given as input to index 0 which has id 1 
    
    db.commit()

    return post_query.first()

@router.delete("/{id}", response_model=Post)
def delete_post(id:int, db : Session = Depends(get_db), current_user : int = Depends(current_user)):
    #index = find_index_post(id)
    #my_posts.pop(index)

    #cursor.execute("delete from posts where id = %s returning *", (str(id))) #rerturning should be written when data is not directly fetched like posting or deleting or updating
    #deleted_post = cursor.fetchone()
    #conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id) # this stores the query not the post
    
    post = post_query.first() # first stores the first instance of the result of query, so use this to get values


    #first need to check if id is present or not (imp)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} is not found")
    if post.owner_id != current_user.id: #this will make sure data fetched is related to the person logged in
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="not authorize to update this post")
    
    post_query.delete(synchronize_session=False)
    #The synchronize_session=False argument means that the session will not be aware of this deletion. It won't keep track of the Post object after the deletion
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) 
    
