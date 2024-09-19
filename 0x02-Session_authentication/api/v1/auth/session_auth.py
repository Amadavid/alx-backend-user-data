#!/usr/bin/env python3
"""
    Module implementing SessionAuth class

"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session class that inherits from Auth class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for given user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns user ID based on session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None):
        """Returns User ID based on the cookie _my_session_id"""
        if request is None:
            return None

        cookie_value = self.session_cookie(request)
        if cookie_value is None:
            return None

        user_id = self.user_id_for_session_id(cookie_value)

        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes user session and logs out user"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
