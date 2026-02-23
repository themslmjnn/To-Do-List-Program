from fastapi import APIRouter, Depends, Path, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy.orm import Session

from passlib.context import CryptContext

from starlette import status
from typing import Annotated
from datetime import timedelta

from db.database import get_db
from core.security import get_current_user
from services import auth_services
from services.token_services import create_access_token
from schemas.auth_schemas import UserResponse, UserUpdate, UserUpdatePassword, Token, UserCreatePublic

from services.auth_services import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

MESSAGE_401 = "Could not validate user"


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_users_by_id(
        db: db_dependency,
        user: user_dependency,
        user_id: Annotated[int, Path(ge=1)]):
    
    return AuthService.get_user_by_id(db, user, user_id)


@router.post("/user_registration", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def add_users(
        db: db_dependency, 
        user_request: UserCreatePublic):
    return AuthService.register_user(db, user_request, bcrypt_context)


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user_by_id(
        db: db_dependency,
        user: user_dependency, 
        user_request: UserUpdate, 
        user_id: Annotated[int, Path(ge=1)]):
    
    return AuthService.update_user_by_id(db, user, user_request, user_id)


@router.put("/{user_id}/password_updating", status_code=status.HTTP_204_NO_CONTENT)
def update_user_password(
        db: db_dependency,
        user: user_dependency, 
        user_request: UserUpdatePassword, 
        user_id: Annotated[int, Path(ge=1)]):

    AuthService.update_user_password(db, user, user_request, user_id)


@router.post("/token", response_model=Token)
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
        db: db_dependency):
    
    user = auth_services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=MESSAGE_401)
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}