from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from Blog import token, database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = token.verify_token(data, credentials_exception)
    user = await database.users_collection.find_one({"email": email})
    if not user:
        raise credentials_exception
    user["id"] = str(user["_id"])
    return user
