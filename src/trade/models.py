from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.db.database import Base


class Trade(Base):
    __tablename__ = 'trade'
    id = Column(Integer, primary_key=True)
    buyer = Column(Integer, ForeignKey("user.id"), primary_key=True)
    offer_buyer = Column(Integer, ForeignKey('offer.id'))
    quantity_buyer = Column(Integer)
    price_buyer = Column(Float)
    price_total_for_buyer = Column(Float)
    seller = Column(Integer, ForeignKey("user.id"))
    offer_seller = Column(Integer, ForeignKey('offer.id'))
    quantity_seller = Column(Integer)
    price_seller = Column(Float)
    total_price_for_seller = Column(Float)

    user_buyer = relationship('User', foreign_keys=[buyer])
    user_seller = relationship('User', foreign_keys=[seller])

    offers_buyer = relationship('Offer', foreign_keys=[offer_buyer])
    offers_seller = relationship('Offer', foreign_keys=[offer_seller])
