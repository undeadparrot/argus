import datetime

from argus_event_log import model

from .base import Handler
from pyramid.view import view_config, view_defaults


@view_defaults(route_name="topics")
class TopicsHandler(Handler):
    @view_config(accept="application/json", renderer="json")
    @view_config(accept="text/html", renderer="topics.mako")
    def get(self):
        session = self.request.registry.make_session()
        topics = session.query(model.Topic).all()
        session.close()
        return dict(
            topics=topics,
            now=datetime.datetime.now()
        )

