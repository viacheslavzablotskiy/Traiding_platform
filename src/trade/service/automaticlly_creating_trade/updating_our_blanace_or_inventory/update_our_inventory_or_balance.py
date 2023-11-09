from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models.models import Inventory, Balance


class UpdateOurAll:

    @classmethod
    async def updating_data_at_all(cls, current_offer, offer_seller, summa_quantity, summa_payment,
                                   user_id_seller: int, user_id_buyer: int,
                                   db_session: AsyncSession):
        query_get_inventory_for_seller = select(Inventory).where(Inventory.user_id == user_id_seller)
        query_get_inventory_for_buyer = select(Inventory).where(Inventory.user_id == user_id_buyer)
        query_get_balance_for_seller = select(Balance).where(Balance.user_id == user_id_seller)
        query_get_balance_for_buyer = select(Balance).where(Balance.user_id == user_id_buyer)

        result_get_inventory_seller = (await db_session.execute(query_get_inventory_for_seller)).scalars().first()
        print(result_get_inventory_seller)
        result_get_inventory_buyer = (await db_session.execute(query_get_inventory_for_buyer)).scalars().first()
        print(result_get_inventory_buyer)
        result_get_balance_for_seller = (await db_session.execute(query_get_balance_for_seller)).scalars().first()
        print(result_get_balance_for_seller)
        result_get_balance_for_buyer = (await db_session.execute(query_get_balance_for_buyer)).scalars().first()
        print(result_get_balance_for_buyer)

        result_get_inventory_seller.amount = result_get_inventory_seller.amount - summa_quantity
        result_get_inventory_buyer.amount = result_get_inventory_buyer.amount + summa_quantity
        result_get_balance_for_seller.balance = result_get_balance_for_seller.balance + summa_payment
        result_get_balance_for_buyer.balance = result_get_balance_for_buyer.balance - summa_payment

        await db_session.commit()



updating_data = UpdateOurAll()
