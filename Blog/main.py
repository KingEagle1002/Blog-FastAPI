from fastapi import FastAPI
from .route import blog, user ,authentication

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)