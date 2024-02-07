#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Use the bcrypt package to perform the hashing (with hashpw)

    Args:
        password (str): one string argument name

    Returns:
        bytes: salted, hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Use bcrypt to validate that the provided password
        matches the hashed password

    Args:
        hashed_password (bytes): bytes type
        password (str): string type

    Returns:
        bool: _description_
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
