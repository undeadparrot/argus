import logging
import collections
import json, uuid
import multiprocessing

import argus_event_log
import argus_event_log.model
import pyramid
from pyramid.config import Configurator
import waitress
import arrow
import abc

import sqlalchemy
import sqlalchemy.orm


def includeme(config):
    engine = sqlalchemy.create_engine('postgresql://argus:argus@localhost/argus')
    make_session = sqlalchemy.orm.sessionmaker(engine)
    config.registry.make_session = make_session
    config.registry.event_queue = multiprocessing.Queue()

    config.include("pyramid_debugtoolbar")
    config.include("pyramid_mako")
    config.add_settings(
        {
            "mako.directories": "argus_event_log:templates",
            "pyramid.reload_templates": "true",
        }
    )
    config.add_route("events", "/events")
    config.add_route("topics", "/topics")
    config.scan("argus_event_log.handlers")


def serve():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    config = Configurator()
    config.include(includeme)
    app = config.make_wsgi_app()
    waitress.serve(app, port=9000, threads=20)


if __name__ == "__main__":
    serve()
