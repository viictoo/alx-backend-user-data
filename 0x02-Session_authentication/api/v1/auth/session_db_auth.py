#!/usr/bin/env python3
"""add an expiration date to a Session ID"""

from .session_exp_auth import SessionExpAuth
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """authentication class based on Session ID stored in database
    """

    def __init__(self) -> None:
        super().__init__()
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """that creates and stores new instance
        of UserSession and returns the Session ID
        """
        pass

    def user_id_for_session_id(self, session_id=None):
        """that returns the User ID by requesting
        UserSession in the database
        based on session_id"""
        pass

    def destroy_session(self, request=None):
        """
        destroys the UserSession based on the Session ID
        from the request cookie
        """
        pass
