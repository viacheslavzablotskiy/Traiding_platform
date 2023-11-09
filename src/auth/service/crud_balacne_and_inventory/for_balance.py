from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models.models import Balance


async def get_balance(db:
AsyncSession,
                      user_id: int, ):
    query = select(Balance).where(Balance.id == user_id)
    result = await db.execute(query)
    return result.scalars().first()
