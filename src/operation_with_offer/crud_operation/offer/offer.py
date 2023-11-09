from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.operation_with_offer.models.offer import Offer
from src.operation_with_offer.schemas.offer.offer import CreateOffer, UpdateOffer
from src.trade.service.automaticlly_creating_trade.operation_with_trade import automatic_creation


async def get_all_offers(db_session: AsyncSession):
    query = select(Offer)
    result = (await db_session.execute(query)).scalars().all()
    return result


async def createtion_the_offer_itself(user_id: int,
                                      db_session: AsyncSession,
                                      obj_in: CreateOffer):
    query_count = select(Offer)
    result = (await db_session.execute(query_count)).scalars().all()
    len_line = len(result)
    obj_in = CreateOffer(id=len_line + 1, user_id=user_id, role_id=obj_in.role_id, quantity=obj_in.quantity,
                         price=obj_in.price,
                         item=obj_in.item)

    query_creating = insert(Offer).values(**obj_in.dict())

    await db_session.execute(query_creating)

    await db_session.commit()

    await automatic_creation.get_all_offer(db_session=db_session)

    query = select(Offer).where(Offer.id == obj_in.id)

    result = (await db_session.execute(query)).scalars().first()

    return result


async def updating_this_offer_by_id(offer_id: int,
                                    obj_in: UpdateOffer,
                                    db_session: AsyncSession):
    query = select(Offer).where(Offer.id == offer_id)

    result_query = (await db_session.execute(query)).scalars().first()

    result_query.quantity = obj_in.quantity
    result_query.role_id = obj_in.role_id
    result_query.price = obj_in.price
    result_query.item = obj_in.item

    await db_session.commit()

    query_for_get = select(Offer).where(Offer.id == offer_id)
    result_to_get = (await db_session.execute(query_for_get)).scalars().first()

    return result_to_get
