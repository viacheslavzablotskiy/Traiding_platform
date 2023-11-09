from typing import List

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models.models import User
from src.auth.service.access_token.access_token import get_current_user
from src.db.database import get_db
from src.operation_with_offer.crud_operation.offer.offer import get_all_offers, createtion_the_offer_itself, \
    updating_this_offer_by_id
from src.operation_with_offer.crud_operation.offer.role import get_all_roles
from src.operation_with_offer.models.offer import Offer
from src.operation_with_offer.schemas.offer.offer import CreateOffer, UpdateOffer
from src.operation_with_offer.schemas.offer.role import CreateRole

router = APIRouter()


@router.get('/all_roles', response_model=List[CreateRole])
async def get_all_roles_for_me(db_session: AsyncSession = Depends(get_db)):
    result = await get_all_roles(db_session=db_session)

    return result


@router.get('/get_all_offer', response_model=List[CreateOffer])
async def get_all_offers_for_me(db_session: AsyncSession = Depends(get_db)):
    result = await get_all_offers(db_session=db_session)

    return result


# @router.get('/get_all_offer_by_user', response_model=CreateOffer)
# async def get_all_offers_for_me_by_user(db_session: AsyncSession = Depends(get_db),
#                                         ):
#     query = select(Offer).where(Offer.user_id is 1)
#     result = (await db_session.execute(query)).scalars().first()
#
#     return  result


@router.post('/create_offer', response_model=CreateOffer)
async def create_offer_for_user(obj_in: CreateOffer,
                                current_user: User = Depends(get_current_user),
                                db_session: AsyncSession = Depends(get_db)):
    current_user_id = jsonable_encoder(current_user)
    get_id_current_user = current_user_id.get('id')

    result = await createtion_the_offer_itself(user_id=get_id_current_user,
                                               obj_in=obj_in,
                                               db_session=db_session)

    return result


@router.put('/updating_the_offer_itself/{offer_id}', response_model=CreateOffer)
async def updaitng_the_offer_offer_itself(offer_id: int,
                                          obj_in: UpdateOffer,
                                          db_session: AsyncSession = Depends(get_db)):
    result = await updating_this_offer_by_id(offer_id=offer_id, obj_in=obj_in,
                                             db_session=db_session)

    return result
