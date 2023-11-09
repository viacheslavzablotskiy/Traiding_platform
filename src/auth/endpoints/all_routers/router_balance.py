from fastapi import APIRouter, Depends
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models.models import User, Balance
from src.auth.schemas.balance import CreateBalance
from src.auth.service.access_token.access_token import get_current_user
from src.auth.service.crud_balacne_and_inventory.for_balance import get_balance
from src.db.database import get_db

router = APIRouter()


@router.get('/balance', response_model=CreateBalance)
async def get_mine_balance(db_session: AsyncSession = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    current_user = jsonable_encoder(current_user)
    get_mine_id = current_user.get('id')

    result = await get_balance(db=db_session, user_id=get_mine_id)

    return result


@router.get('/{user_id}', response_model=CreateBalance)
async def get_balance_by_id(user_id: int,
                            db:
                            AsyncSession = Depends(get_db),
                            ):
    query = select(Balance).where(Balance.id == user_id)
    result = await db.execute(query)
    return result.scalars().first()

