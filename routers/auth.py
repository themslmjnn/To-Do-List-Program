from fastapi import APIRouter, Depends, Path, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from starlette import status

from typing import Annotated

from passlib.context import CryptContext

from datetime import timedelta

from db.database import get_db
from repositories.auth_repository import UserRepository
from services import auth_services
from schemas.auth_schemas import UserCreate, UserResponse, UserUpdate, UserUpdatePassword, Token

from models.user_model import Users
from services.token_services import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

db_dependency = Annotated[Session, Depends(get_db)]


MESSAGE_404 = "User(s) not found"
MESSAGE_409 = "Duplicate values are not accepted"
MESSAGE_401 = "Could not validate user"


@router.get("", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(db: db_dependency):
    return UserRepository.get_all_users(db)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_users_by_id(db: db_dependency, user_id: int = Path(ge=1)):
    user_model = UserRepository.get_user_by_id(db, user_id)

    if user_model is None:
        raise HTTPException(status_code=404, detail=MESSAGE_404)
    
    return user_model


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_users_by_id(db: db_dependency, user_id: int = Path(ge=1)):
    user_model = UserRepository.get_user_by_id(db, user_id)

    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    UserRepository.delete_user_by_id(db, user_model)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def add_users(db: db_dependency, user_request: UserCreate):
    new_user = Users(\
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
        return UserRepository.add_user(db, new_user)
    
    except IntegrityError:
        db.rollback()

        raise HTTPException(status_code=409, detail=MESSAGE_409)
    

@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user_by_id(db: db_dependency, user_request: UserUpdate, user_id: int = Path(ge=1)):
    user_model = UserRepository.get_user_by_id(db, user_id)

    if user_model is None:
        raise HTTPException(status_code=404, detail=MESSAGE_404)
    
    try:
        for field, value in user_request.model_dump(exclude_unset=True).items():
            setattr(user_model, field, value)

        db.commit()

    except IntegrityError:
        db.rollback()
        
        raise HTTPException(status_code=409, detail=MESSAGE_409)
    
    return user_model

@router.put("/{user_id}/password_updating", status_code=status.HTTP_204_NO_CONTENT)
def update_user_password(db: db_dependency, user_request: UserUpdatePassword, user_id: int = Path(ge=1)):
    user_model = UserRepository.get_user_by_id(db, user_id)

    if user_model is None:
        raise HTTPException(status_code=404, detail=MESSAGE_404)
    
    if not bcrypt_context.verify(user_request.old_password, user_model.hash_password):
        raise HTTPException(status_code=401, detail="Invalid old password")
    
    user_model.hash_password = bcrypt_context.hash(user_request.new_password)

    db.commit()


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = auth_services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=MESSAGE_401)
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}



