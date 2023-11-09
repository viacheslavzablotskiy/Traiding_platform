from fastapi import FastAPI
from sqladmin import Admin, ModelView

from src.auth.endpoints.base_router import api_router
from src.operation_with_offer.endpoint.base_router import api_router as router_operation
from src.trade.enpoints.base_router import api_router as router_trade
from src.auth.models.models import User, Balance, Inventory
from src.db.database import engine
from src.operation_with_offer.models.item import Item, Currency
from src.operation_with_offer.models.offer import Offer, Role
from src.trade.models import Trade

app = FastAPI()

admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.full_name, User.email, User.hashed_password, User.is_active, User.is_superuser]


class UserBalance(ModelView, model=Balance):
    column_list = [Balance.id, Balance.user_id, Balance.balance]


class UserInventory(ModelView, model=Inventory):
    column_list = [Inventory.id, Inventory.user_id, Inventory.amount]


class UserOffer(ModelView, model=Offer):
    column_list = [Offer.id, Offer.user_id, Offer.item, Offer.role_id, Offer.price, Offer.quantity, Offer.is_activate]


class UserRole(ModelView, model=Role):
    column_list = [Role.id, Role.role]


class UserCurrency(ModelView, model=Currency):
    column_list = [Currency.id, Currency.currency]


class UserItem(ModelView, model=Item):
    column_list = [Item.id, Item.currency_id, Item.max_price]


class UserTrade(ModelView, model=Trade):
    column_list = [Trade.id, Trade.buyer, Trade.offer_buyer, Trade.quantity_buyer, Trade.price_buyer,
                   Trade.price_total_for_buyer, Trade.seller, Trade.offer_seller, Trade.quantity_seller,
                   Trade.price_seller, Trade.total_price_for_seller]


admin.add_view(UserAdmin)
admin.add_view(UserBalance)
admin.add_view(UserInventory)
admin.add_view(UserRole)
admin.add_view(UserCurrency)
admin.add_view(UserItem)
admin.add_view(UserOffer)
admin.add_view(UserTrade)

app.include_router(api_router)
app.include_router(router_operation)
app.include_router(router_trade)
