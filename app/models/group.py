from datetime import date, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint
# from sqlalchemy.orm import backref, relationship

from app.db.base_class import Base


class Groups(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group = Column(String(50), index=True, unique=True)
