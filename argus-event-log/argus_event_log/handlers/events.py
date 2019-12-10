import datetime
import json
from argus_event_log import model

from .base import Handler
from pyramid.view import view_config, view_defaults


@view_defaults(route_name="events")
class EventsHandler(Handler):
    @view_config(accept="text/html", renderer="events.mako")
    def get(self):
        session = self.request.registry.make_session()
        return dict(
            events=model.Event.get_recent(session)
        )

    @view_config(accept="application/json", renderer="json", request_method='POST')
    @view_config(accept="text/html", renderer="events.mako", request_method='POST')
    def post(self):
        try:
            json_body = json.loads(self.data['body'])
        except ValueError:
            return dict(error="Event body must be valid JSON")
        session = self.request.registry.make_session()
        events = model.Event.get_recent(session)
        event = model.Event.create(
            session,
            topic_name=self.data['topic'],
            body=json_body,
        )
        session.add(event)
        session.commit()
        return dict(
            created_event=event,
            events=events
        )

