from fastapi import status, HTTPException
from Blog import database
from Blog.schemas import Blog
from bson import ObjectId

# MongoDB blogs collection
blogs_collection = database.blogs_collection


# Get all blogs
async def get_all():
    blogs = []
    cursor = blogs_collection.find({})
    async for blog in cursor:
        blog["_id"] = str(blog["_id"]) 
        blogs.append(blog)
    return blogs


# Create new blog
async def create(request: Blog, user_id: str = "1"):
    new_blog = {
        "title": request.title,
        "body": request.body,
        "user_id": user_id
    }
    result = await blogs_collection.insert_one(new_blog)
    new_blog["_id"] = str(result.inserted_id)
    return new_blog


# Delete a blog
async def destroy(id: str):
    blog = await blogs_collection.find_one({"_id": ObjectId(id)})
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found"
        )

    await blogs_collection.delete_one({"_id": ObjectId(id)})
    return {"message": "Blog deleted successfully"}


# Update a blog
async def update(id: str, request: Blog):
    blog = await blogs_collection.find_one({"_id": ObjectId(id)})
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found"
        )

    await blogs_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"title": request.title, "body": request.body}}
    )
    return {"message": "Blog updated successfully"}


# Get single blog
async def show(id: str):
    blog = await blogs_collection.find_one({"_id": ObjectId(id)})
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found"
        )
    blog["_id"] = str(blog["_id"])
    return blog
