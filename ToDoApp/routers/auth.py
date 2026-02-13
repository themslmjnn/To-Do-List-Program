from fastapi import APIRouter, Depends, Path, HTTPException
from pydantic_schemas import UserCreate, UserResponse, Token
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from database import get_db
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta

import models


router = APIRouter()

SECRET_KEY = "3b3604d053ceb6d9cb36d4b5b4ae5ff7bc927b426980619591a72cee62cb79dd"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/auth", response_model=list[UserResponse], status_code=status.HTTP_200_OK, tags=["Get Methods"])
async def get_all_users(db: db_dependency):
    return db.query(models.Users).all()


@router.get("/auth/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, tags=["Search Methods"])
async def get_users_by_id(db: db_dependency, user_id: int = Path(ge=1)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_model


@router.delete("/auth/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Delete Methods"])
async def delete_users_by_id(db: db_dependency, user_id: int = Path(ge=1)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user_model)
    db.commit()


@router.post("/auth", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Add Methods"])
async def add_users(db: db_dependency, user_request: UserCreate):
    new_user = models.Users(\
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        date_of_birth=user_request.date_of_birth,
        email_address=user_request.email_address,
        hash_password=bcrypt_context.hash(user_request.password),
        role=user_request.role,
        is_active=user_request.is_active
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(new_user.hash_password)
        return new_user
    except IntegrityError:
        db.rollback()

        raise HTTPException(status_code=409, detail="Duplicate values are not accepted")
    

@router.put("/auth/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, tags=["Update Methods"])
async def update_users_by_id(db: db_dependency, user_request: UserCreate, user_id: int = Path(ge=1)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        for field, value in user_request.model_dump().items():
            setattr(user_model, field, value)

        db.commit()
    except IntegrityError:
        db.rollback()
        
        raise HTTPException(status_code=409, detail="Duplicate values are not accepted")
    
    return user_model

def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users).filter(models.Users.username == username).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hash_password):
        return False
    
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}
