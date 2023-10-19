#following code is copied from fastapi > relational databses website
#this is database configurations
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# SQLALCHEMY_DATABASE_URL = "driver_adapter://<ussername>:<password>@<ipaddress/hostname>/<database_name>"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL #connect_args={"check_same_thread": False} # connect_args is paramtere sued only for sql lite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#dependency - creating a session and it will be called for every request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#we have now connected our database to python using sql alchemy