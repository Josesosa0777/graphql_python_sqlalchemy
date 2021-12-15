import logging.config
from dependency_injector import containers, providers
from microservice.core.interfaces.db import DBAdapter
from microservice.adapters.db.connection import Database
from microservice.adapters.db.implementation import DB
from microservice.core.actions import Actions
from microservice.adapters.web import create_app


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()
    log = providers.Resource(logging.config.dictConfig, config=config.logging)
    db_conn = providers.Singleton(Database, db_url=config.db.connection_string)
    database = providers.Factory(DB, session_factory=db_conn.provided.session)
    actions = providers.Factory(Actions, config=config, db=database)
    web_app = providers.Factory(create_app, config=config.web, actions=actions)
