from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models.models import Inventory, Balance
from src.operation_with_offer.models.offer import Offer

from src.trade.service.automaticlly_creating_trade.creation_trade_depending_on_the_number.if_current_iffer_has_less_shares\
    import offer_seller_more
from src.trade.service.automaticlly_creating_trade.creation_trade_depending_on_the_number.if_current_offer_and_offer_seller_have_the_same_number \
    import the_same_of_number
from src.trade.service.automaticlly_creating_trade.creation_trade_depending_on_the_number.if_current_offer_has_more_shares import \
    current_offer_has_more


class AutomaticCreationTrade:

    @classmethod
    async def get_all_offer(cls, db_session: AsyncSession):
        query = select(Offer).where(Offer.role_id == 2)
        result = (await db_session.execute(query)).scalars().all()
        print(jsonable_encoder(result))
        for offer in result:
            offer_price = offer.price
            print(jsonable_encoder(offer_price))
            await cls.get_necessary_offer_for_users(offer_price=offer_price, offer=offer,
                                                     db_session=db_session)


    @classmethod
    async def get_necessary_offer_for_users(cls, offer, offer_price: float, db_session: AsyncSession):
        query = select(Offer).where(Offer.role_id == 1, Offer.price >= offer_price)
        result_1 = (await db_session.execute(query)).scalars().first()
        print(result_1)
        if result_1:
            user_id_seller = int(jsonable_encoder(result_1).get('user_id'))
            user_id_buyer = int(jsonable_encoder(offer).get('user_id'))
            await cls.get_all_tools(user_id_seller=user_id_seller, user_id_buyer=user_id_buyer,
                                    current_offer=offer, db_session=db_session, offer_seller=result_1)

    @classmethod
    async def get_all_tools(cls, user_id_seller: int, user_id_buyer: int, offer_seller,
                            current_offer, db_session: AsyncSession):
        query_get_inventory_for_seller = select(Inventory).where(Inventory.user_id == user_id_seller)
        result_query_inv_for_seller = (await db_session.execute(query_get_inventory_for_seller)).scalars().first()
        query_get_inventory_for_buyer = select(Inventory).where(Inventory.user_id == user_id_buyer)
        result_query_inv_for_buyer = (await db_session.execute(query_get_inventory_for_buyer)).scalars().first()
        query_get_balance_for_seller = select(Balance).where(Balance.user_id == user_id_seller)
        result_query_bl_for_seller = (await db_session.execute(query_get_balance_for_seller)).scalars().first()
        query_get_balance_for_buyer = select(Balance).where(Balance.user_id == user_id_seller)
        result_query_bl_for_buyer = (await db_session.execute(query_get_balance_for_buyer)).scalars().first()

        if (current_offer.is_activate is True and offer_seller.is_activate is True) and (
                result_query_bl_for_buyer.balance > offer_seller.quantity * offer_seller.price
        ):
            await cls.make_trade(current_offer=current_offer, offer_seller=offer_seller,
                                 inv_seller=result_query_inv_for_seller,
                                 inv_buyer=result_query_inv_for_buyer,
                                 bal_seller=result_query_bl_for_seller,
                                 bal_buyer=result_query_bl_for_buyer,
                                 db_session=db_session)
        else:
            current_offer.is_activate = False
            await db_session.commit()

    @classmethod
    async def make_trade(cls, current_offer, offer_seller,
                         inv_seller, inv_buyer, bal_seller, bal_buyer,
                         db_session: AsyncSession):
        if current_offer.quantity > offer_seller.quantity:
            await current_offer_has_more.if_current_offer_and_offer_seller_has_the_same_number_of_shares(
                current_offer=current_offer,
                offer_seller=offer_seller,
                inv_seller=inv_seller,
                inv_buyer=inv_buyer,
                bal_seller=bal_seller,
                bal_buyer=bal_buyer,
                db_session=db_session
                )

            await db_session.commit()
        elif current_offer.quantity < offer_seller.quantity:
            await offer_seller_more.if_current_offer_has_fewer_shares(current_offer=current_offer,
                                                                      offer_seller=offer_seller,
                                                                      inv_buyer=inv_buyer,
                                                                      inv_seller=inv_seller,
                                                                      bal_buyer=bal_buyer,
                                                                      bal_seller=bal_seller,
                                                                      db_session=db_session)

            await db_session.commit()
        elif current_offer.quantity == offer_seller.quantity:
            await the_same_of_number.if_current_offer_and_offer_seller_has_the_same_number_of_shares(
                current_offer=current_offer,
                offer_seller=offer_seller,
                inv_buyer=inv_buyer,
                inv_seller=inv_seller,
                bal_buyer=bal_buyer,
                bal_seller=bal_seller,
                db_session=db_session
            )

            await db_session.commit()

automatic_creation = AutomaticCreationTrade()