from typing import List
from pydantic import BaseModel

class HPData(BaseModel):
    headline: str

class PostData(BaseModel):
    id: int
    title: str
    content: str

class PostsData(BaseModel):
    data: List[PostData]