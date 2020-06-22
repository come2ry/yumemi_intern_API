from datetime import date, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import backref, relationship

from app.db.base_class import Base


class Words(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(50))
    groupId = Column(Integer, ForeignKey('groups.id'))

    group = relationship(
        'groups',
        backref=backref('words',
                        lazy="select",
                        cascade='delete,all')
    )

    __table_args__ = (
        UniqueConstraint('word','groupId'),
        Index('word_and_groupId_idx', word, groupId),
        {},
    )