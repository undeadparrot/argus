
from sqlalchemy import Column, ForeignKey, String, Integer, JSON, DateTime, UniqueConstraint, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.type_api import Variant
import sqlalchemy.ext.declarative

from typing import List

Base = sqlalchemy.ext.declarative.declarative_base()

class Topic(Base):
    __tablename__ = 'topic'
    id = Column('topic_id', String, primary_key=True)
    created_date = Column(DateTime, nullable=False)

class Event(Base):
    __tablename__ = 'event'
    id = Column('event_id', Integer, primary_key=True)
    uuid = Column(UUID, nullable=False)
    body = Column(JSON, nullable=False)
    event_date = Column(DateTime, nullable=False) # date event was sent
    created_date = Column(DateTime, nullable=False) # date event was added to db
    topic_id = Column('topic_id', ForeignKey(Topic.id), nullable=False)

class Consumer(Base):
    __tablename__ = 'consumer'
    id = Column('consumer_id', String, primary_key=True)
    name = Column(String, nullable=False)
    pattern = Column(String, nullable=False)
    offset_date = Column(DateTime, nullable=False)
    UniqueConstraint(name, pattern)
