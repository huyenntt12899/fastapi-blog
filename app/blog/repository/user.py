
from blog import schemas, models
from fastapi import status, HTTPException, Depends
from sqlalchemy.orm import Session
from blog.hashing import Hash

def create(request: schemas.User, db: Session):
    hashed_password = Hash.get_password_hash(request.password)
    request.password = hashed_password
    new_user = models.User(**request.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The user with the id {id} is not found')
    return user