from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.operation_with_offer.models.offer import Role


async def get_all_roles(db_session: AsyncSession):
    query = select(Role)
    result = (await db_session.execute(query)).scalars().all()
    return result
