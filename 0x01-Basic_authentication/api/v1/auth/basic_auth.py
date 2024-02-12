#!/usr/bin/env python3
""" Module of basic auth views
"""
from .auth import Auth
import base64


class BasicAuth(Auth):
    """Basic Auth"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Basic - Base64 part
         returns the Base64 part of the Authorization header 
         for a Basic Authentication"""
        if (authorization_header is None or
            type(authorization_header) is not str or
                not authorization_header.startswith("Basic ")):
            return None
        return (authorization_header[6:])

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns the decoded value of a base64 string"""
        if (base64_authorization_header is None or
                type(base64_authorization_header) is not str):
            return None
        try:
            # print(base64_authorization_header)
            # return base64_authorization_header.decode('utf-8')
            return base64.b64decode(base64_authorization_header).decode()
        except Exception:
            return None
