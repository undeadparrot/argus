import logging
import collections
import dataclasses
import json, uuid
import pyramid
from pyramid.config import Configurator
import waitress
import arrow
import abc

from sqlalchemy import Column, ForeignKey, String, Integer, JSON, DateTime, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.type_api import Variant
import sqlalchemy.ext.declarative

from typing import List

Base = sqlalchemy.ext.declarative.declarative_base()

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    uuid = Column(String().with_variant(UUID, 'postgresql'), nullable=False)
    body = Column(JSON, nullable=False)
    created_date = Column(DateTime, nullable=False)



def ensure_db_exists():
    db = sqlite3.connect("events.db")
    cursor = db.cursor()

    cursor.execute(
        """
     CREATE TABLE IF NOT EXISTS topic ( 
        topic_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL UNIQUE  
    ) """
    )
    cursor.execute(
        """
     CREATE TABLE IF NOT EXISTS event ( 
        event_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        event_uuid UUID NOT NULL UNIQUE, 
        topic_id INTEGER NOT NULL REFERENCES topics(topic_id), 
        body TEXT NOT NULL, 
        created_date DATETIME DEFAULT CURRENT_TIMESTAMP 
    ) """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS consumer (
        consumer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        topic TEXT NOT NULL,
        last_event_id INTEGER NOT NULL DEFAULT 0,
        created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(name, topic)
    ) """
    )

    cursor.close()
    db.commit()
    db.close()


def get_topic_id(cursor, name: str):
    get_query = """
        SELECT topic_id 
        FROM topic 
        WHERE name = :name
    """
    insert_query = """
        INSERT INTO topic (name) 
        VALUES (:name)
    """
    row = cursor.execute(get_query, {"name": name}).fetchone()
    if not row:
        cursor.execute(insert_query, {"name": name})
    row = cursor.execute(get_query, {"name": name}).fetchone()
    return row[0]


def insert_event(cursor, topic, body):
    insert_query = """
        INSERT INTO event (event_uuid, topic_id, body) 
        VALUES (:event_uuid, :topic_id, :body)
    """
    event_uuid = str(uuid.uuid4())
    topic_id = get_topic_id(cursor, topic)
    cursor.execute(
        insert_query,
        {"event_uuid": event_uuid, "topic_id": topic_id, "body": json.dumps(body)},
    )
    return event_uuid


def get_next_consumer_event(cursor, name: str, topic: str):
    get_query = """
        SELECT last_event_id 
        FROM consumer 
        WHERE name = :name
        AND topic = :topic
    """
    insert_query = """
        INSERT INTO consumer (name, topic) 
        VALUES (:name, :topic)
    """
    row = cursor.execute(get_query, {"name": name, "topic": topic}).fetchone()
    if not row:
        cursor.execute(insert_query, {"name": name, "topic": topic})
    row = cursor.execute(get_query, {"name": name, "topic": topic}).fetchone()
    last_event_id = row[0]

    get_event_query = """
        SELECT event_id, event_uuid, topic_id, topic.name, created_date, body 
        FROM event JOIN topic USING (topic_id) 
        WHERE event_id > :last_event_id 
        AND topic.name LIKE :topic
        ORDER BY event_id ASC 
        LIMIT 1
    """
    update_consumer_query = """
        UPDATE consumer 
        SET last_event_id = :event_id 
        WHERE consumer.name = :name
        AND topic = :topic
    """
    row = cursor.execute(
        get_event_query, {"last_event_id": last_event_id, "topic": topic}
    ).fetchone()
    if row:
        cursor.execute(
            update_consumer_query, {"name": name, "topic": topic, "event_id": row[0]}
        ).fetchone()

    logging.debug("get_event %s", row)
    return (
        {
            "event_uuid": row[1],
            "topic_id": row[2],
            "topic_name": row[3],
            "timestamp": arrow.get(row[4]).isoformat(),
            "body": json.loads(row[5]),
        }
        if row
        else None
    )


def post_events(request):
    data = json.loads(request.body)
    topic = request.matchdict["topic"]
    body = data

    db = sqlite3.connect("events.db")
    cursor = db.cursor()

    try:
        insert_event(cursor, topic, body)
    except Exception:
        logging.exception("post_events")
    finally:
        cursor.close()
        db.commit()
        db.close()

    return pyramid.response.Response()


def get_events(request):
    consumer_name = request.params["consumer"]
    topic = request.matchdict["topic"]
    db = sqlite3.connect("events.db")
    cursor = db.cursor()

    try:
        event_dict = get_next_consumer_event(cursor, consumer_name, topic)

        if event_dict:
            return pyramid.response.Response(json=event_dict)
    except Exception:
        logging.exception("get_events")
    finally:
        cursor.close()
        db.commit()
        db.close()

    return pyramid.response.Response(status=204)


def get_topics(request):
    query = """
    SELECT 
        topic.topic_id,
        topic.name,
        count(event.event_id),
        max(event.event_id)
    FROM topic
    JOIN event USING (topic_id)
    GROUP BY topic.topic_id
    """
    db = sqlite3.connect("events.db")
    cursor = db.cursor()
    cursor.execute(query)
    topics_dict = [
        {"id": row[0], "name": row[1], "length": row[2], "offset": row[3]}
        for row in cursor.fetchall()
    ]
    return pyramid.response.Response(json=topics_dict)


def get_consumers(request):
    query = """
    SELECT 
        consumer.consumer_id,
        consumer.name,
        consumer.topic,
        consumer.last_event_id
    FROM consumer
    """
    db = sqlite3.connect("events.db")
    cursor = db.cursor()
    cursor.execute(query)
    consumers_dict = [
        {"id": row[0], "name": row[1], "topic_filter": row[2], "offset": row[3]}
        for row in cursor.fetchall()
    ]
    return pyramid.response.Response(json=consumers_dict)


def make_wsgi():
    config = Configurator()
    config.add_route("topics", "/topics")
    config.add_route("consumers", "/consumers")
    config.add_route("events_topic", "/events/{topic}")
    config.add_view(post_events, route_name="events_topic", request_method="POST")
    config.add_view(get_events, route_name="events_topic")
    config.add_view(get_topics, route_name="topics")
    config.add_view(get_consumers, route_name="consumers")
    ensure_db_exists()
    return config.make_wsgi_app()


def serve():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    app = make_wsgi()
    waitress.serve(app)


if __name__ == "__main__":
    serve()
