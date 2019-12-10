import datetime
import secrets
import uuid

from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    JSON,
    DateTime,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.type_api import Variant
import sqlalchemy.ext.declarative

from typing import List

Base = sqlalchemy.ext.declarative.declarative_base()


class Topic(Base):
    __tablename__ = "topic"
    id = Column("topic_id", String, primary_key=True)
    created_date = Column(DateTime, nullable=False, server_default="now()")


class Event(Base):
    __tablename__ = "event"
    id = Column("event_id", Integer, primary_key=True)
    uuid = Column(UUID, nullable=False, unique=True)
    body = Column(JSON, nullable=False)
    # date event was sent
    event_date = Column(
        DateTime, nullable=False, default=lambda: datetime.datetime.now()
    )
    # date event was added to db
    created_date = Column(DateTime, nullable=False, server_default="now()")
    topic_id = Column("topic_id", ForeignKey(Topic.id), nullable=False)
    topic = relationship("Topic")

    @classmethod
    def create(cls, session, topic_name, body):
        topic = session.query(Topic).get(topic_name)
        if not topic:
            topic = Topic(id=topic_name)
        return Event(topic=topic, body=body, uuid=str(uuid.uuid4()))

    @classmethod
    def get_recent(cls, session):
        return session.query(Event).order_by(Event.event_date.desc()).limit(5).all()

class Consumer(Base):
    __tablename__ = "consumer"
    id = Column("consumer_id", String, primary_key=True)
    name = Column(String, nullable=False)
    pattern = Column(String, nullable=False)
    token = Column(String, nullable=False)
    created_date = Column(DateTime, nullable=False, server_default="now()")
    UniqueConstraint(name, pattern)
    UniqueConstraint(token)

    @classmethod
    def create(cls, name, pattern):
        return Consumer(name=name, pattern=pattern, token=secrets.token_bytes(20))

    @classmethod
    def by_token(cls, session, token):
        consumer = session.query(cls).where(cls.token == token).first()
        return consumer
