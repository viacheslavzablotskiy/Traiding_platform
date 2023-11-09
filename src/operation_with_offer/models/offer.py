from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.db.database import Base


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    role = Column(String)

    offer = relationship('Offer', back_populates='role')

    def __repr__(self):
        return f'{self.role}'


class Offer(Base):
    __tablename__ = 'offer'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    role_id = Column(Integer, ForeignKey('role.id'))
    quantity = Column(Integer)
    price = Column(Float)
    item = Column(Integer, ForeignKey('item.id'))
    is_activate = Column(Boolean, default=True)

    user = relationship('User', back_populates='offer')
    items = relationship('Item', back_populates='offer')
    role = relationship('Role', back_populates='offer')



