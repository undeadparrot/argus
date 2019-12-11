import datetime
import json
import time

import pyramid.response
from argus_event_log import model

from .base import Handler
from pyramid.view import view_config, view_defaults


@view_defaults(route_name="events")
class EventsHandler(Handler):
    @view_config(accept="text/html", renderer="events.mako")
    def get(self):
        session = self.request.registry.make_session()
        return dict(events=model.Event.get_recent(session))

    @view_config(accept="text/event-stream")
    def get_event_stream(self):
        session = self.request.registry.make_session()
        latest_event = (
            session.query(model.Event).order_by(model.Event.id.desc()).first()
        )
        def event_generator():
            last_id = latest_event.id if latest_event else 0
            for topic_name in model.listen_for_notify(session.connection()):
                events = (
                    session.query(model.Event)
                    .filter(model.Event.topic_id == topic_name)
                    .filter(model.Event.id > last_id)
                    .order_by(model.Event.id.asc())
                    .all()
                )
                for event in events:
                    yield ("type: event\ndata: %s\n\n" % event.body).encode()
                last_id = events[-1].id
                session.flush()

        return pyramid.response.Response(
            app_iter=event_generator(), content_type="text/event-stream"
        )

    @view_config(accept="application/json", renderer="json", request_method="POST")
    @view_config(accept="text/html", renderer="events.mako", request_method="POST")
    def post(self):
        try:
            json_body = json.loads(self.data["body"])
        except ValueError:
            return dict(error="Event body must be valid JSON")
        session = self.request.registry.make_session()
        events = model.Event.get_recent(session)
        event = model.Event.create(
            session, topic_name=self.data["topic"], body=json_body
        )
        session.add(event)
        session.commit()
        return dict(created_event=event, events=events)
