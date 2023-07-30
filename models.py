from typing import List
from pydantic import BaseModel

class HPData(BaseModel):
    headline: str

class Post(BaseModel):
    id: int
    title: str
    content: str

class PostDataRes(BaseModel):
    res: str
    data: Post

class PostsDataRes(BaseModel):
    res: str
    data: List[Post]


class CreatePost(BaseModel):
    title: str
    content: str

class DeleteResponse(BaseModel):
    message: str
