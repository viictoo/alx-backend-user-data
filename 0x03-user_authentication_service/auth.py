#!/usr/bin/env python3
"""user authentication module"""
from bcrypt import hashpw, gensalt
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
        return ValueError('User {} already exists'.format(email))
