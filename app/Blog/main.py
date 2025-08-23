from fastapi import FastAPI
from .Blog import models
from .Blog.database import engine
from .Blog.route import blog , user , authentication

app = FastAPI()


# Create tables
models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)


























# -------------------- Blog Endpoints --------------------

# Get all blogs
# @app.get('/blog', response_model=List[schemas.ShowBlog], tags=['Blogs'])
# def All(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs

# Create a new blog
# @app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['Blogs'])
# def create(request: schemas.Blog, db: Session = Depends(get_db)):
#     new_blog = models.Blog(
#         title=request.title,
#         body=request.body,
#         user_id = 1
#     )
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog    

# Get a single blog by ID
# @app.get('/blog/{id}', response_model=schemas.ShowBlog, tags=['Blogs'])
# def Show(id: int, response: Response, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if not blog:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Blog with id {id} not found")
#     return blog

# # Delete a blog by ID
# @app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blogs'])
# def delete(id: int, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Blog with id {id} not found")
#     blog.delete(synchronize_session=False)
#     db.commit()
#     return {'detail': 'Blog deleted successfully'}

# # Update a blog by ID
# @app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blogs'])
# def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Blog with id {id} not found")
#     blog.update(request.dict())
#     db.commit()
#     return {'detail': 'Blog updated successfully'}

# -------------------- User Endpoints --------------------

# Create a new user
# @app.post('/user', response_model=schemas.ShowUser, tags=['Users'])
# def create_user(request: schemas.User, db: Session = Depends(get_db)):
#     hashed_password = Hash.bcrypt(request.password)
#     new_user = models.User(
#         name=request.name,
#         email=request.email,
#         password=hashed_password,
        
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# Get a user by ID
# @app.get('/user/{id}', response_model=schemas.ShowUser, tags=['Users'])
# def get_user(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"User with id {id} not found")
#     return user
