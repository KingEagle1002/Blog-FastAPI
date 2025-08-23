from fastapi import  APIRouter , Depends
from .. import schemas, database
from sqlalchemy.orm import Session
from ..repository import user





router = APIRouter(
    prefix="/User",
    tags=['Users']
)
get_db = database.get_db


# -------------------- User Endpoints --------------------

# Create a new user
@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)

# Get a user by ID
@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db) 