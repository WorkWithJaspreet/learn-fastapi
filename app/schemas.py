from pydantic import BaseModel, EmailStr
from datetime import datetime


# # Created a model for the post using BaseModel from Pydantic
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     # rating: Optional[int] = None  # Optional field


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None  # Optional field


class PostCreate(PostBase):
    pass


# class Post(BaseModel):
class Post(PostBase):
    id: int  # This is needed to tell the user his/her post id after creating the post in case when he needs to update or delete the post
    # title: str # We can inherit these fields from PostBase class instead of redefining them here
    # content: str
    # published: bool
    # created_at: str  # Datetime
    created_at: datetime  # Better to use datetime object than string and we are fetching it as our frontend may need to do some operations on it

    # class Config: # This was needed to convert the SQLAlchemy model to a Pydantic model as Pydantic by default only works with dictionaries, and don't know how to read SQLAlchemy/ORM models/objects
    #     orm_mode = True # This method was used in Pydantic v1

    # model_config = {  # This is used in Pydantic v2 to read data from ORM models/objects and it converts it to a dictionary automatically
    #     "from_attributes": True  # This is equivalent to orm_mode = True in Pydantic v1
    # }  # Though this is not needed as we are using response_model in the route decorator which automatically does this conversion for us, but it's good to know about it as it's gives clarity about how Pydantic works with ORM models/objects


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
