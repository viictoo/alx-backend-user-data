#!/usr/bin/env python3
"""add an expiration date to a Session ID"""

from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
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
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kwargs = {"user_id": user_id, "session_id": session_id}
        userSesh = UserSession(**kwargs)
        userSesh.save()
        userSesh.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """that returns the User ID by requesting
        UserSession in the database
        based on session_id"""
        if not session_id:
            return None

        UserSession.load_from_file()
        userSesh = UserSession.search({'session_id': session_id})

        if not userSesh:
            return None

        user = userSesh[0]

        expiredTime = (user.created_at +
                       timedelta(seconds=self.session_duration))

        if expiredTime < datetime.utcnow():
            return None

        return user.user_id

    def destroy_session(self, request=None):
        """
        destroys the UserSession based on the Session ID
        from the request cookie
        """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()
            UserSession.save_to_file()
            return True
        return False
