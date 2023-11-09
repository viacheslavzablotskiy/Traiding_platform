from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.db.database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    balance = relationship('Balance', back_populates='user')
    inventory = relationship('Inventory', back_populates='users')
    offer = relationship('Offer', back_populates='user')


    def __repr__(self):
        return f'{self.full_name}'


class Balance(Base):
    __tablename__ = 'balance'
    id = Column(Integer, primary_key=True)
    balance = Column(Float)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship('User', back_populates='balance')

    def __repr__(self):
        return f'{self.user_id}: balance - {self.balance}'


class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))

    users = relationship('User', back_populates='inventory')

    def __repr__(self):
        return f'{self.user_id}: amount - {self.amount}'
