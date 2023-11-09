from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.operation_with_offer.crud_operation.item.currency import get_all_currency
from src.operation_with_offer.crud_operation.item.item import get_all_items
from src.operation_with_offer.schemas.item.currency import CreateCurrency
from src.operation_with_offer.schemas.item.item import CreateItem

router = APIRouter()


@router.get('/get_all_currency', response_model=List[CreateCurrency])
async def get_all_currencies(db_session: AsyncSession = Depends(get_db)):
    result = await get_all_currency(db_session=db_session)

    return result


@router.get('/get_all_items', response_model=List[CreateItem])
async def get_all_items_for_user(db_session: AsyncSession = Depends(get_db)):
    result = await get_all_items(db_session=db_session)

    return result
