from pydantic import BaseModel, EmailStr
from typing import Optional, List

# ----------------- Blog -----------------
class Blog(BaseModel):
    title: str
    body: str

class ShowBlog(Blog):
    id: str
    class Config:
        orm_mode = True

# ----------------- User -----------------
class User(BaseModel):
    name: str
    email: EmailStr
    password: str

class ShowUser(BaseModel):
    id: str
    name: str
    email: EmailStr
    blogs: Optional[List[Blog]] = []

    class Config:
        orm_mode = True
