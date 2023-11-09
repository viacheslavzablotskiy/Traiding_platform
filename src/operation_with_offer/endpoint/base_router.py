from fastapi import APIRouter

from src.operation_with_offer.endpoint.all_router import item, offer

api_router = APIRouter()

api_router.include_router(offer.router, prefix='/offer', tags=['offer'])
api_router.include_router(item.router, prefix='/item', tags=['item'])
