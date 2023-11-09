from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.auth.models.models import Inventory


async def get_mine_inventory(user_id: int,
                             db_session: AsyncSession):
    query = select(Inventory).where(Inventory.id == user_id)
    result = await db_session.execute(query)

    return result.scalars().first()


async def get_mine_inventory_by_id(inventory_id: int,
                                   db_session: AsyncSession):
    query = select(Inventory).where(Inventory.id == inventory_id)
    result = await db_session.execute(query)

    return result.scalars().first()
