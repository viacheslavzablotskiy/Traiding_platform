from typing import Optional

from pydantic import BaseModel


class BaseTrade(BaseModel):
    buyer: Optional[int] = None
    offer_buyer: Optional[int] = None
    quantity_buyer: Optional[int] = None
    price_buyer: Optional[float] = None
    price_total_for_buyer: Optional[float] = None
    seller: Optional[int] = None
    offer_seller: Optional[int] = None
    quantity_seller: Optional[int] = None
    price_seller: Optional[float] = None
    total_price_for_seller: Optional[float] = None


class IdTrade(BaseTrade):
    id: int

    class Config:
        orm_mode = True


class CreateTrade(IdTrade):
    pass
