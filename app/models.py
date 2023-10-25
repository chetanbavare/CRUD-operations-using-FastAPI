#this is table configuration

from time import timezone
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id =Column(Integer, primary_key=True, nullable =  False)
    title =Column(String, nullable =  False)
    content =Column(String, nullable =  False)
    published =Column(Boolean, server_default='TRUE', nullable=False) #server default value has to be a string
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False )
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner_of_the_post = relationship("Users") # sets a relation between post and owner ,now we can fetch details of user who posted inside the post he posted


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True) #order is important
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    phone_num = Column(String, nullable=False)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, primary_key=True)