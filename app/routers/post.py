from fastapi import Response, status, HTTPException, Depends, APIRouter  # , FastAPI
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db


router = APIRouter(
    prefix="/posts"
)


# FastAPI goes line by line and runs the first path operation along with the http method that matches the request
# So the order of the path operations matter
# @router.get("")
@router.get("", response_model=List[schemas.Post])
# def get_posts():
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()

    # print(posts)
    # return {"data": posts}
    return posts


# @router.get("/{id}")
@router.get("/{id}", response_model=schemas.Post)
# def get_post(id: int, response: Response):
# def get_post(id: int):
def get_post(id: int, db: Session = Depends(get_db)):
    # post = find_post(id)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        # response.status_code = 404
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": f"Post with {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} was not found")
    # print(post)
    # return {"data": post}
    return post


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# Take everything from the request body, convert it to the dictionary and put it in payload
# def create_post(payload: dict = Body(...)):
# def create_post(post: schemas.PostBase):  # Referencing the Post model
# def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # We expect the payload to have title: str and content: str
    # print(post)  # print(payload)
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(
        # title=post.title, content=post.content, published=post.published
        **post.dict()  # This does the same thing as above (unpacking the dictionary)
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # return {"data": new_post}
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
def delete_post(id: int, db: Session = Depends(get_db)):
    # index = find_index_post(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with {id} was not found")
    # my_posts.pop(index)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    # if deleted_post == None:
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} was not found")
    # conn.commit()
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.put("/{id}")
@router.put("/{id}", response_model=schemas.Post)
# def update_post(id: int, post: schemas.PostBase):
# def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db)):
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # index = find_index_post(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with {id} was not found")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} was not found")
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    # conn.commit()
    # return {"data": updated_post.first()}
    return updated_post.first()
