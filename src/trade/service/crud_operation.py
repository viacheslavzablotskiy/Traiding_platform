from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.trade.models import Trade


async def get_all_trades(db_session: AsyncSession):
    query = select(Trade)

    result = (await db_session.execute(query)).scalars().all()

    return result
