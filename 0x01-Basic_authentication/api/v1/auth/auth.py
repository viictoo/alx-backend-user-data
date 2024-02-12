#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from typing import TypeVar, List


class Auth:
    """class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False"""
        if not path or not excluded_paths or excluded_paths == []:
            return True
        if not path.endswith('/'):
            path = path + '/'

        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns None"""

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None"""

        return None
