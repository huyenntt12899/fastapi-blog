from fastapi import APIRouter, Depends, HTTPException, status
from blog import schemas, database, models
from sqlalchemy.orm import Session
from blog.hashing import Hash
from typing import Annotated
from blog.routers import token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(request: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if (not user or not Hash.verify_password(request.password,user.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials', headers={"WWW-Authenticate": "Bearer"})
    
    # access_token_expires = timedelta(minutes=token.ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = token.create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)
    access_token = token.create_access_token(data={'sub': user.email})
    return schemas.Token(access_token=access_token, token_type='bearer')