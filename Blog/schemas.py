from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from bson import ObjectId

# ✅ Custom ObjectId type
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Blog Schema
class Blog(BaseModel):
    title: str
    body: str
    user_id: Optional[str]  # MongoDB ObjectId as string


class ShowBlog(Blog):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# User Schema
class User(BaseModel):
    name: str
    email: EmailStr
    password: str

class ShowUser(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    email: EmailStr
    blogs: Optional[List[ShowBlog]] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
