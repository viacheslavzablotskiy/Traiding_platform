from typing import List

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas.inventory import CreateInventory

from src.auth.models.models import User, Inventory
from src.auth.service.access_token.access_token import get_current_user
from src.db.database import get_db
from src.auth.service.crud_balacne_and_inventory.for_inventory import get_mine_inventory, get_mine_inventory_by_id

router = APIRouter()


@router.get('/inventory', response_model=CreateInventory)
async def get_inventory(db_session: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    get_mine_current_user = jsonable_encoder(current_user)
    get_current_user_id = get_mine_current_user.get('id')

    result = await get_mine_inventory(db_session=db_session, user_id=get_current_user_id)

    return result


@router.get('/inventory/{user_id}', response_model=CreateInventory)
async def get_inventory_by_id(user_id: int, db_session: AsyncSession = Depends(get_db)):

    result = await get_mine_inventory_by_id(inventory_id=user_id, db_session=db_session)

    return result


