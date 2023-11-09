from pydantic import BaseModel
from typing import Optional


class BaseCurrency(BaseModel):
    id: int
    currency: Optional[str] = None


class CreateCurrency(BaseCurrency):
    pass