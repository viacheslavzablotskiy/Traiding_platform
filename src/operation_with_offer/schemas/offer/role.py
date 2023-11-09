from pydantic import BaseModel
from typing import Optional


class BaseRole(BaseModel):
    id: int
    role: Optional[str] = None


class CreateRole(BaseRole):
    pass
