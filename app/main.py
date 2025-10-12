from fastapi import FastAPI  # , Response, status, HTTPException, Depends
# from fastapi.params import Body
# from typing import Optional
# from typing import List
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
# from sqlalchemy.orm import Session
from . import models  # , schemas, utils
from .database import engine  # , get_db
from .routers import auth, post, user


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed!")
        print("Error: ", error)
        time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
    "title": "title of post 2", "content": "content of post 2", "id": 2}]


def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# Path operation
@app.get("/")  # Path operation decorator with the path and operation type
def root():  # Path operation function
    # This will be converted to JSON automatically
    return {"message": "Welcome to the App!"}


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}
