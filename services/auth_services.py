from repositories import auth_repository
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def authenticate_user(username: str, password: str, db):
    user = auth_repository.AuthRepo.get_user_by_username(db, username)

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hash_password):
        return False
    
    return user