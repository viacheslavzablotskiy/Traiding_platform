from fastapi import APIRouter

from src.trade.enpoints.all_routers import enpoint

api_router = APIRouter()


api_router.include_router(enpoint.router, prefix='/trade', tags=['trade'])