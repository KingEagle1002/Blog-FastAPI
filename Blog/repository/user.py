from fastapi import status, HTTPException
from Blog.hash import Hash
from Blog import database
from Blog.schemas import User
from bson import ObjectId

# MongoDB users collection
users_collection = database.users_collection


# Create a new user
async def create(request: User):
    new_user = {
        "name": request.name,
        "email": request.email,
        "password": Hash.bcrypt(request.password)
    }

    # Check if user already exists
    existing_user = await users_collection.find_one({"email": request.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    result = await users_collection.insert_one(new_user)
    new_user["_id"] = str(result.inserted_id)
    return new_user


# Get user by ID
async def show(id: str):
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )

    user["_id"] = str(user["_id"])
    return user
