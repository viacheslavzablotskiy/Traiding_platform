from typing import Optional

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service.crud_user.service import CRUDBase
from src.auth.models.models import User
from src.auth.schemas.schemas import UserUpdate, UserCreate
from src.auth.service.crud_user.creating_balance_and_inventory import create_balance_after_user, \
    create_inventory_after_user
from src.auth.utils import verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    async def get_by_email(self, db_session: AsyncSession, *, email: str) -> Optional[User]:
        result = select(User).where(User.email == email)
        query = await db_session.execute(result)
        return query.scalars().first()

    async def create(self, db_session: AsyncSession, *, obj_in: UserCreate):
        all_user = select(User)
        all_user_1 = await db_session.execute(all_user)
        x = len(all_user_1.scalars().all())
        obj_in = UserCreate(id=x + 1, full_name=obj_in.full_name, email=obj_in.email,
                            hashed_password=obj_in.hashed_password)
        db_obj = insert(User).values(**obj_in.dict())

        await db_session.execute(db_obj)
        await db_session.commit()
        obj_in_test = select(User).where(User.id == obj_in.id)
        obj_in_test_1 = await db_session.execute(obj_in_test)

        await create_balance_after_user(db=db_session, obj_in=obj_in)

        await create_inventory_after_user(db=db_session, obj_in=obj_in)

        return obj_in_test_1.scalars().first()

    async def authenticate(
            self, db_session: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
        user = await self.get_by_email(db_session, email=email)
        if not user:
            return None
        if not await verify_password(password, user.hashed_password):
            return None
        return user

    async def is_active(self, user: User) -> bool:
        return user.is_active

    async def is_superuser(self, user: User) -> bool:
        return user.is_superuser


crud_user = CRUDUser(User)
