from pydantic import BaseModel


class BaseItem(BaseModel):
    currency_id: int
    max_price: float


class IDItem(BaseItem):
    id: int

    class Config:
        orm_mode = True


class CreateItem(IDItem):
    pass