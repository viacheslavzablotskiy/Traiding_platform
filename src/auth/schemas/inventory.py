from pydantic import BaseModel


class BaseInventory(BaseModel):
    amount: int
    user_id: int


class BaseIDInventory(BaseInventory):
    id: int

    class Config:
        orm_mode = True


class CreateInventory(BaseIDInventory):
    pass
