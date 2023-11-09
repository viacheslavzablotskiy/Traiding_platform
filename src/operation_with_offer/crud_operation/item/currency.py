from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.operation_with_offer.models.item import Currency


async def get_all_currency(db_session: AsyncSession):
    query = select(Currency)
    result = (await db_session.execute(query)).scalars().all()
    return result