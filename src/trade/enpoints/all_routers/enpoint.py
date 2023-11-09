from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.trade.schemas import CreateTrade
from src.trade.service.crud_operation import get_all_trades

router = APIRouter()


@router.get('/get_all_trades', response_model=List[CreateTrade])
async def get_all_trade_for_users(db_session: AsyncSession = Depends(get_db)):
    result = await get_all_trades(db_session=db_session)

    return result
