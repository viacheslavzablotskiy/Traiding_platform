from fastapi import Depends, Security, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN
from src.auth.models.models import User
from src.auth.service.utils import crud_user
from src.db.config import ALGORITHM, SECRET_KEY
from src.auth.schemas.token import TokenPayload

from src.db.database import get_db

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")


async def get_current_user(
        db: AsyncSession = Depends(get_db), token: str = Security(reusable_oauth2)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = await crud_user.get(db, id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(current_user: User = Security(get_current_user)):
    if not crud_user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(current_user: User = Security(get_current_user)):
    if not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
