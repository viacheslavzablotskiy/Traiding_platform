from typing import List
from sqlalchemy import select
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service.access_token.access_token import get_current_active_superuser, get_current_active_user, \
    get_current_user

from src.db.database import get_db

from src.auth.models.models import User as DBUser
from src.auth.schemas.schemas import User, UserUpdate, UserCreate, UserInDB
from src.auth.service.utils import crud_user
from src.auth.utils import get_password_hash

router = APIRouter()


@router.get("/", response_model=List[User])
async def read_users(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100,

):
    """
    Retrieve users.
    """
    users = await crud_user.get_multi(db, skip=skip, limit=limit)
    print(len(users))
    return users


@router.get("/delete/{user_id}", response_model=List[User])
async def delete_users(
        user_id: int,
        db: AsyncSession = Depends(get_db),

):
    results = await crud_user.remove(db_session=db, id=user_id)
    return results.scalars().all()


@router.post("/open", response_model=User)
async def create_user_open(
        *,
        db: AsyncSession = Depends(get_db),
        password: str = Body(...),
        email: EmailStr = Body(...),
        full_name: str = Body(None),
):
    """
    Create new user without the need to be logged in.
    """
    user = await crud_user.get_by_email(db_session=db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = UserCreate(hashed_password=password, email=email, full_name=full_name)
    user = await crud_user.create(db_session=db, obj_in=user_in)
    return user


@router.post("/", response_model=User)
async def create_user(
        *,
        db: AsyncSession = Depends(get_db),
        user_in: UserCreate,

):
    """
    Create new user.
    """
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user_in = UserCreate(full_name=user_in.full_name,
                         email=user_in.email, hashed_password=await get_password_hash(user_in.hashed_password, ))
    user = await crud_user.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=User)
async def update_user_me(
        *,
        db: AsyncSession = Depends(get_db),
        password: str = Body(None),
        full_name: str = Body(None),
        email: EmailStr = Body(None),
        current_user: DBUser = Depends(get_current_user),
):
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = await crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=User)
async def read_user_me(
        db: AsyncSession = Depends(get_db),
        current_user: DBUser = Depends(get_current_active_user),
):
    get_current_user_id = jsonable_encoder(current_user)
    print(get_current_user_id.get('id'))
    """
    Get current user.
    """
    return current_user


@router.get("/{user_id}", response_model=User)
async def read_user_by_id(
        user_id: int,
        current_user: DBUser = Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db),
):
    """
    Get a specific user by id.
    """
    user = await crud_user.get(db, id=user_id)
    if user == current_user:
        return user
    if not await crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(
        *,
        db: AsyncSession = Depends(get_db),
        user_id: int,
        user_in: UserUpdate,
        current_user: DBUser = Depends(get_current_active_superuser),
):
    """
    Update a user.
    """
    user = await crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = await crud_user.update(db, db_obj=user, obj_in=user_in)
    return user
