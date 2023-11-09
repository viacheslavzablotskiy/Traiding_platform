from typing import List, Optional, Generic, TypeVar, Type

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.db.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db_session: AsyncSession, id: int):
        result = select(self.model).where(self.model.id == id)
        result = await db_session.execute(result)
        return result.scalars().first()

    #
    # # def get_users(self, db_session: Session, id: int) -> Optional[ModelType]:
    # #     return db_session.q(self.model).filter(self.model.id == id).first()

    async def get_multi(self, db_session: AsyncSession, *, skip=0, limit=100):
        result = select(self.model).limit(limit)
        query = await db_session.execute(result)
        return query.scalars().all()

    async def create(self, db_session: AsyncSession, *, obj_in: CreateSchemaType):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = insert(self.model).values(**obj_in_data.dict())
        # db_obj = await self.model(**obj_in_data)
        await db_session.execute(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def update(
            self, db_session: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        print(obj_data)
        update_data = obj_in.dict()
        print(update_data)
        for field in obj_data:
            if field in update_data:
                print(field)
                setattr(db_obj, field, update_data[field])
        print(jsonable_encoder(db_obj))
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def remove(self, db_session: AsyncSession, *, id: int):
        obj = select(self.model).where(self.model.id == id)
        query = await db_session.execute(obj)
        await db_session.delete(query.scalars().first())
        await db_session.commit()
        result = select(self.model)
        result_1 = await db_session.execute(result)
        return result_1
