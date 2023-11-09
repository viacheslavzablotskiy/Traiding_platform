from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.operation_with_offer.models.item import Item



async def get_all_items(db_session: AsyncSession):
    query = select(Item)
    result = (await db_session.execute(query)).scalars().all()
    return result