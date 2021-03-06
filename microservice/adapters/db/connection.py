from contextlib import contextmanager, AbstractContextManager
from typing import Callable
import logging

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class Database:

    def __init__(self, db_url: str) -> None:
        logging.info("Init database connection class")
        self._engine = create_engine(db_url, echo=True, future=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        logging.info("Session creation")
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logging.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
