from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.trade.models import Trade
from src.trade.schemas import CreateTrade

from src.trade.service.automaticlly_creating_trade.updating_our_blanace_or_inventory.update_our_inventory_or_balance \
    import updating_data


class OfferSEqualCoffer:

    @classmethod
    async def if_current_offer_and_offer_seller_has_the_same_number_of_shares(cls, current_offer,
                                                                              offer_seller,
                                                                              inv_seller,
                                                                              inv_buyer,
                                                                              bal_seller,
                                                                              bal_buyer, db_session: AsyncSession):
        query_for_find_out_number_trades = select(Trade)
        result_query_for_creation = (
            await db_session.execute(query_for_find_out_number_trades)).scalars().all()
        len_our_list = len(result_query_for_creation) + 1

        quantity_trade = current_offer.quantity
        price_trade = offer_seller.price / current_offer.quantity
        total_price = quantity_trade * price_trade

        schema_for_creation_trade = CreateTrade(id=len_our_list,
                                                buyer=current_offer.user_id,
                                                offer_buyer=current_offer.id,
                                                quantity_buyer=quantity_trade,
                                                price_buyer=price_trade,
                                                total_offer_buyer=total_price,
                                                seller=offer_seller.user_id,
                                                offer_seller=offer_seller.id,
                                                quantity_seller=quantity_trade,
                                                price_seller=price_trade,
                                                total_price_for_seller=total_price
                                                )
        query_for_creation = insert(Trade).values(**schema_for_creation_trade.dict())

        await db_session.execute(query_for_creation)

        current_offer.is_activate = False
        offer_seller.is_activate = False


        user_id_seller = int(jsonable_encoder(offer_seller).get('user_id'))
        user_id_buyer = int(jsonable_encoder(current_offer).get('user_id'))

        await updating_data.updating_data_at_all(current_offer=current_offer,
                                                 offer_seller=offer_seller,
                                                 summa_quantity=quantity_trade,
                                                 summa_payment=total_price,
                                                 user_id_seller=user_id_seller,
                                                 user_id_buyer=user_id_buyer,
                                                 db_session=db_session)

        await db_session.commit()


the_same_of_number = OfferSEqualCoffer()
