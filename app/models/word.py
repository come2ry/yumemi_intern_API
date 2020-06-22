from datetime import date, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint
# from sqlalchemy.orm import backref, relationship

from app.db.base_class import Base


class Word(Base):
    __table_args__ = (UniqueConstraint('word','group'),{})
    id = Column(Integer, primary_key=True)
    word = Column(String, index=True)
    group = Column(String, index=True)
