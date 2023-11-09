from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from src.db.database import Base


class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True)
    currency = Column(String)

    item = relationship('Item', back_populates='currency')

    def __repr__(self):
        return f'{self.currency}'


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    currency_id = Column(Integer, ForeignKey('currency.id'))
    max_price = Column(Float)

    currency = relationship('Currency', back_populates='item')
    offer = relationship('Offer', back_populates='items')

    def __repr__(self):
        return f'{self.currency_id}'


