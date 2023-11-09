from fastapi import APIRouter

from src.auth.endpoints.all_routers import users, user_login, router_balance, router_inventory

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(user_login.router, tags=["login"])
api_router.include_router(router_inventory.router, tags=["inventory"])
api_router.include_router(router_balance.router, tags=["balance"])



