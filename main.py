from fastapi import FastAPI
# from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


# Created a model for the post using BaseModel from Pydantic
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# Path operation
@app.get("/")  # Path operation decorator with the path and operation type
def root():  # Path operation function
    # This will be converted to JSON automatically
    return {"message": "Welcome to my API!"}


# FastAPI goes line by line and runs the first path operation along with the http method that matches the request
# So the order of the path operations matter
@app.get("/posts")
def get_posts():
    return {"data": "These are your posts."}


@app.post("/createposts")
# Take everything from the request body, convert it to the dictionary and put it in payload
# def create_posts(payload: dict = Body(...)):
def create_posts(new_post: Post):  # Referencing the Post model
    # We expect the payload to have title: str and content: str
    print(new_post)  # print(payload)
    return {"data": "new_post"}
