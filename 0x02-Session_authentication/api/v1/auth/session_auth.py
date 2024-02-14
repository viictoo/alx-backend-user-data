#!/usr/bin/env python3
""" Module of session auth views
"""
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """Basic User Auth"""
    pass
