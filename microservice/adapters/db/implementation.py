import logging
import bcrypt
from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from microservice.core.interfaces.db import DBAdapter

from .model import User


class DB(DBAdapter):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        logging.info("Init db implementation")
        self.session_factory = session_factory
        logging.info('db object created')

    def list_users(self):
        with self.session_factory() as session:
            try:
                users_list = session.query(User).all()
                users = [user.to_dict() for user in users_list]
                payload = {
                    "success": True,
                    "users": users
                }
            except Exception as error:
                payload = {
                    "success": False,
                    "errors": [str(error)]
                }
            return payload

    def get_user(self, user_id):
        with self.session_factory() as session:
            try:
                user = session.query(User).get(user_id)
                payload = {
                    "success": True,
                    "user": user
                }
            except Exception as error:
                payload = {
                    "success": False,
                    "errors": [str(error)]
                }
            return payload

    def new_user(self, email, password):
        with self.session_factory() as session:
            try:
                hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
                user = User(email=email, hashed_password=hashed_password, is_active=True)
                session.add(user)
                session.commit()
                session.refresh(user)
                payload = {
                    "success": True,
                    "user": user
                }
            except Exception as error:
                session.rollback()
                payload = {
                    "success": False,
                    "errors": [str(error)]
                }
            return payload

    def check_user_passwd(self, email, password):
        with self.session_factory() as session:
            try:
                user = session.query(User).filter(User.email == email).first()
                if bcrypt.checkpw(password.encode("UTF-8"), user.hashed_password):
                    payload = {
                        "success": True,
                        "same": True
                    }
                else:
                    payload = {
                        "success": True,
                        "same": False
                    }
            except Exception as error:
                payload = {
                    "success": False,
                    "error": error
                }
            return payload

    def delete_user(self, user_id):
        pass

    def dummy(self):
        pass
