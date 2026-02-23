from fastapi import Depends, HTTPException
from typing import Annotated
from db.config import settings
from starlette import status

from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')

MESSAGE_401 = "Could not validate user"

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=MESSAGE_401)
        
        return {'username': username, 'id': user_id, 'user_role': user_role}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=MESSAGE_401)