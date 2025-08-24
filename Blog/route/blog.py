from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from bson import ObjectId
from Blog import schemas, database, oauth2

router = APIRouter(prefix="/Blog", tags=["Blogs"])
blogs_collection = database.blogs_collection

@router.get("/", response_model=List[schemas.ShowBlog])
async def all_blogs(current_user: dict = Depends(oauth2.get_current_user)):
    blogs = []
    async for blog in blogs_collection.find({}):
        blog["_id"] = str(blog["_id"])
        blogs.append(blog)
    return blogs

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_blog(request: schemas.Blog, current_user: dict = Depends(oauth2.get_current_user)):
    blog_data = request.dict()
    blog_data["user_id"] = str(current_user["id"])
    result = await blogs_collection.insert_one(blog_data)
    return {"id": str(result.inserted_id), "message": "Blog created"}

@router.get("/{id}", response_model=schemas.ShowBlog)
async def show_blog(id: str, current_user: dict = Depends(oauth2.get_current_user)):
    blog = await blogs_collection.find_one({"_id": ObjectId(id)})
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    blog["_id"] = str(blog["_id"])
    return blog

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: str, current_user: dict = Depends(oauth2.get_current_user)):
    result = await blogs_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    return {"detail": "Blog deleted successfully"}

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_blog(id: str, request: schemas.Blog, current_user: dict = Depends(oauth2.get_current_user)):
    updated_data = request.dict()
    result = await blogs_collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    return {"detail": "Blog updated successfully"}
