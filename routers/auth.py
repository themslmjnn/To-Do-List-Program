from fastapi import APIRouter, Depends, Path, HTTPException
from schemas.pydantic_schemas import UserCreate, UserResponse, Token
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from db.database import get_db
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta

import models.models as models
from repositories import auth_repository
from services import auth_services


router = APIRouter()

SECRET_KEY = "3b3604d053ceb6d9cb36d4b5b4ae5ff7bc927b426980619591a72cee62cb79dd"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

db_dependency = Annotated[Session, Depends(get_db)]


MESSAGE_404 = "User(s) not found"
MESSAGE_409 = "Duplicate values are not accepted"
MESSAGE_401 = "Could not validate user"

@router.get("/auth", response_model=list[UserResponse], status_code=status.HTTP_200_OK, tags=["Get Methods"])
def get_all_users(db: db_dependency):
    return auth_repository.AuthRepo.get_all_users(db)


@router.get("/auth/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, tags=["Search Methods"])
def get_users_by_id(db: db_dependency, user_id: int = Path(ge=1)):
    user_model = auth_repository.AuthRepo.get_user_by_id(db, user_id)

    if user_model is None:
        raise HTTPException(status_code=404, detail=MESSAGE_404)
    
    return user_model


@router.delete("/auth/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Delete Methods"])
def delete_users_by_id(db: db_dependency, user_id: int = Path(ge=1)):
    user_model = auth_repository.AuthRepo.get_user_by_id(db, user_id)

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    auth_repository.AuthRepo.delete_user_by_id(db, user_model)


@router.post("/auth", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Add Methods"])
def add_users(db: db_dependency, user_request: UserCreate):
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
        return auth_repository.AuthRepo.add_user(db, new_user)
    except IntegrityError:
        db.rollback()

        raise HTTPException(status_code=409, detail=MESSAGE_409)
    

@router.put("/auth/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, tags=["Update Methods"])
def update_users_by_id(db: db_dependency, user_request: UserCreate, user_id: int = Path(ge=1)):
    user_model = auth_repository.AuthRepo.get_user_by_id(db, user_id)

    if user_model is None:
        raise HTTPException(status_code=404, detail=MESSAGE_404)
    
    try:
        for field, value in user_request.model_dump().items():
            setattr(user_model, field, value)

        db.commit()
    except IntegrityError:
        db.rollback()
        
        raise HTTPException(status_code=409, detail=MESSAGE_409)
    
    return user_model


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=MESSAGE_401401)
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=MESSAGE_401)


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = auth_services.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=MESSAGE_401)
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}



