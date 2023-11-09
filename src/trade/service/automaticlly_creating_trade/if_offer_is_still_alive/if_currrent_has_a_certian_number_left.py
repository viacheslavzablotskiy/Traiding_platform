from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.operation_with_offer.models.offer import Offer
from src.trade.models import Trade
from src.trade.schemas import CreateTrade
from src.trade.service.automaticlly_creating_trade.updating_our_blanace_or_inventory.update_our_inventory_or_balance import \
    updating_data


class OfferLeft:

    @classmethod
    async def if_current_offer_has_a_certain_number(cls, current_offer,
                                                    inv_seller,
                                                    price_current_offer: float,
                                                    inv_buyer,
                                                    bal_seller,
                                                    bal_buyer, db_session: AsyncSession):

        print(price_current_offer)
        query = select(Offer).where(Offer.price <= price_current_offer, Offer.is_activate == True,
                                    Offer.role_id == 1)
        result = (await db_session.execute(query)).scalars().all()
        print(result)

        if result:

            for offer_seller in result:

                if current_offer.quantity != 0:

                    query_for_find_out_number_trades = select(Trade)
                    result_query_for_creation = (
                        await db_session.execute(query_for_find_out_number_trades)).scalars().all()
                    len_our_list = len(result_query_for_creation) + 1

                    user_id_seller = int(jsonable_encoder(offer_seller).get('user_id'))
                    user_id_buyer = int(jsonable_encoder(current_offer).get('user_id'))

                    if current_offer.quantity > offer_seller.quantity:
                        quantity_trade = offer_seller.quantity
                        price_trade = offer_seller.price / offer_seller.quantity
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

                        offer_seller.is_activate = False

                        current_offer.quantity = current_offer.quantity - quantity_trade

                        await db_session.execute(query_for_creation)

                        await updating_data.updating_data_at_all(current_offer=current_offer,
                                                                 offer_seller=offer_seller,
                                                                 summa_quantity=quantity_trade,
                                                                 summa_payment=price_trade,
                                                                 user_id_seller=user_id_seller,
                                                                 user_id_buyer=user_id_buyer,
                                                                 db_session=db_session)

                        await db_session.commit()

                        if current_offer.quantity != 0:
                            continue

                    elif current_offer.quantity < offer_seller.quantity:
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

                        current_offer.is_activate = False

                        offer_seller.quantity = offer_seller.quantity - quantity_trade

                        await db_session.execute(query_for_creation)

                        await updating_data.updating_data_at_all(current_offer=current_offer,
                                                                 offer_seller=offer_seller,
                                                                 summa_quantity=quantity_trade,
                                                                 summa_payment=price_trade,
                                                                 user_id_seller=user_id_seller,
                                                                 user_id_buyer=user_id_buyer,
                                                                 db_session=db_session)

                        await db_session.commit()

                    elif current_offer.quantity == offer_seller.quantity:
                        quantity_trade = offer_seller.quantity
                        price_trade = offer_seller.price / offer_seller.quantity
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

                        current_offer.is_activate = False
                        offer_seller.is_activate = False

                        await db_session.execute(query_for_creation)

                        await updating_data.updating_data_at_all(current_offer=current_offer,
                                                                 offer_seller=offer_seller,
                                                                 summa_quantity=quantity_trade,
                                                                 summa_payment=price_trade,
                                                                 user_id_seller=user_id_seller,
                                                                 user_id_buyer=user_id_buyer,
                                                                 db_session=db_session)

                        await db_session.commit()
                else:
                    continue


remaining_offer = OfferLeft()
