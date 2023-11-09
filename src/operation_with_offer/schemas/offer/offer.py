from pydantic import BaseModel
from typing import Optional


class BaseOffer(BaseModel):
    user_id: Optional[int] = None
    role_id: Optional[int] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    item: int
    is_activate: Optional[bool] = True


class UpdateOffer(BaseModel):
    role_id: int
    quantity: int
    price: float
    item: int


class IDOffer(BaseOffer):
    id: int

    class Config:
        orm_mode = True


class CreateOffer(IDOffer):
    pass
