# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time


#class Post(BaseModel):      
#    title:str
#    content:str
#    published: bool = True
#    published: bool = True
# this will be placed inside schema.py

# while True: # we are using postgres and cursor object to execute queries for database in postgress
#     try: #cursor factory is used to get column names and their values
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password = 'chetanbavare', cursor_factory=RealDictCursor)
#         cursor = conn.cursor() # an object to take over the database
#         print("database connection successful")
#         break
#     except Exception as error:
#         print("database connection not successful")
#         print("error:" , error)
#         time.sleep(2)

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p    #returns the whole element whose id is same as id given as input 
    
# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i # returns index of the element that has id same as id given as input

#my_posts = [        #this is a temporary array database made inside memory
#     {
#         'title':'title of post 1',
#         'content':'content of post 1',
#         'id': 1
#     },

#     {
#         'title':'favourite foods',
#         'content':'I like pizza',
#         'id': 2
#     },
#     {
#         'title':'title of post 3',
#         'content':'content of post 3',
#         'id': 3
#     },

#     {
#         'title':'not favourite foods',
#         'content':'I hate pizza',
#         'id': 4
#     }
# ]