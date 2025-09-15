from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()


# Created a model for the post using BaseModel from Pydantic
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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


# Path operation
@app.get("/")  # Path operation decorator with the path and operation type
def root():  # Path operation function
    # This will be converted to JSON automatically
    return {"message": "Welcome to my API!"}


# FastAPI goes line by line and runs the first path operation along with the http method that matches the request
# So the order of the path operations matter
@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/{id}")
# def get_post(id: int, response: Response):
def get_post(id: int):
    post = find_post(id)
    if not post:
        # response.status_code = 404
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": f"Post with {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} was not found")
    print(post)
    return {"data": f"Post with {id} is {post}"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
# Take everything from the request body, convert it to the dictionary and put it in payload
# def create_posts(payload: dict = Body(...)):
def create_posts(post: Post):  # Referencing the Post model
    # We expect the payload to have title: str and content: str
    print(post)  # print(payload)
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} was not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": f"Post with id {id} was updated"}
