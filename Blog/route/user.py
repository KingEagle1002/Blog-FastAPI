from fastapi import APIRouter, HTTPException, status
from Blog import schemas, database
from Blog.hash import Hash
from bson import ObjectId
from typing import List

router = APIRouter(
    prefix="/User",
    tags=['Users']
)


users_collection = database.users_collection

# -------------------- Get all users -----------------
@router.get("/", response_model=List[schemas.ShowUser])
async def All_users():
    users = []
    async for user in users_collection.find({}):
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

# -------------------- Create a new user -----------------
@router.post('/', response_model=schemas.ShowUser)
async def create_user(request: schemas.User):
    user_data = request.dict()
    user_data["password"] = Hash.bcrypt(request.password)
    result = await users_collection.insert_one(user_data)
    created_user = await users_collection.find_one({"_id": result.inserted_id})
    created_user["_id"] = str(created_user["_id"])
    return created_user

# -------------------- Get a user by ID -----------------
@router.get('/{id}', response_model=schemas.ShowUser)
async def Show_user(id: str):
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    user["_id"] = str(user["_id"])
    return user

# -------------------- Update a user by ID -----------------
@router.put("/{id}", response_model=schemas.ShowUser)
async def update_user(id: str, request: schemas.User):
    # Check if user exists
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    
    # Prepare updated data
    updated_data = {
        "name": request.name,
        "email": request.email,
        "password": Hash.bcrypt(request.password)  # password ko hash karna
    }
    
    # Update user in DB
    await users_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_data}
    )
    
    # Return updated user
    updated_user = await users_collection.find_one({"_id": ObjectId(id)})
    updated_user["_id"] = str(updated_user["_id"])
    return updated_user

# -------------------- Delete a user by ID -----------------
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    result = await users_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return {"detail": "User deleted successfully"}


