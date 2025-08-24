from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from Blog import database, token, hash

router = APIRouter(tags=["Authentication"], prefix="/Login")
users_collection = database.users_collection

@router.post("/", response_model=None, summary="User Login")
async def login(request: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": request.username})
    if not user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    
    if not hash.Hash.verify(user["password"], request.password):
        raise HTTPException(status_code=404, detail="Incorrect Password")
    
    access_token = token.create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
