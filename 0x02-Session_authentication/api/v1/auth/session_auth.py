#!/usr/bin/env python3
""" Module of session auth views
"""
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Basic User Auth"""

    def __init__(self) -> None:
        super().__init__()

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None

        sessionID = str(uuid4())
        # subscript Notatation
        self.user_id_by_session_id[sessionID] = user_id
        return sessionID
