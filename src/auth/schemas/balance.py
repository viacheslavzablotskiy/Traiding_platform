from pydantic import BaseModel


class BaseBalance(BaseModel):
    balance: float
    user_id: int


class BaseIDBalance(BaseBalance):
    id: int

    class Config:
        orm_mode = True


class CreateBalance(BaseIDBalance):
    pass
