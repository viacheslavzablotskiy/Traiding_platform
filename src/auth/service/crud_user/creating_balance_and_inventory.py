from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models.models import Balance, Inventory
from src.auth.schemas.balance import CreateBalance
from src.auth.schemas.inventory import CreateInventory
from src.auth.schemas.schemas import UserCreate


async def create_balance_after_user(db: AsyncSession,
                                    obj_in: UserCreate,
                                    ):
    schema_for_creating = CreateBalance(id=obj_in.id, user_id=obj_in.id, balance=100)
    query_balance = insert(Balance).values(**schema_for_creating.dict())

    await db.execute(query_balance)
    await db.commit()


async def create_inventory_after_user(db: AsyncSession,
                                      obj_in: UserCreate,
                                      ):
    schema_for_creating_inventory = CreateInventory(id=obj_in.id, user_id=obj_in.id, amount=0)
    query_inventory = insert(Inventory).values(**schema_for_creating_inventory.dict())

    await db.execute(query_inventory)
    await db.commit()
