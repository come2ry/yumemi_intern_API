from datetime import date, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import backref, relationship

from app.db.base_class import Base


class NgWords(Base):
    __tablename__ = 'ng_words'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ng_word = Column(String(50))
    group_id = Column(Integer, ForeignKey('groups.id'))

    group = relationship(
        'Groups',
        backref=backref('ngWords',
                        lazy="select",
                        cascade='delete,all')
    )

    __table_args__ = (
        UniqueConstraint('ng_word','group_id'),
        Index('ng_word_and_group_id_idx', ng_word, group_id),
        {},
    )