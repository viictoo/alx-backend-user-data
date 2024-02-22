#!/usr/bin/env python3
"""user authentication module"""
from bcrypt import hashpw, gensalt, checkpw
from uuid import uuid4

from sqlalchemy.orm.exc import NoResultFound

from db import DB, User


def _hash_password(password: str) -> bytes:
    """
    hashes raw password data with bcrypt
    Args:
        password (str): raw input string
    Returns:
        bytes: salted hash of the input password
    """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """
    hashes raw password data with bcrypt
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a new user given a new password and email
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError(f'User {email} already exists')
        
    def valid_login(self, email: str, password: str) -> bool:
        """registers a new user given a new password and email
        """
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(
                password.encode("utf-8"),
                user.hashed_password
                )
        except NoResultFound:
            return False
    
    def create_session(self, email: str) -> str:
        """registers a new user given a new password and email
        """
        try:
            # ver1
            # in memory storage: lost sessiionif server crashes
            # user = self._db.find_user_by(email=email)
            # user.session_id = _generate_uuid()
            # return user.session_id

            # ver 2
            # imeediate persistent db storage: 
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id = session_id)
            return user.session_id
        
        except NoResultFound:
            return None

    def get_user_from_session_id(self, email: str) -> str:
        """registers a new user given a new password and email
        """
        try:
            # ver1
            # in memory storage: lost sessiionif server crashes
            # user = self._db.find_user_by(email=email)
            # user.session_id = _generate_uuid()
            # return user.session_id

            # ver 2
            # imeediate persistent db storage: 
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id = session_id)
            return user.session_id
        
        except NoResultFound:
            return None
