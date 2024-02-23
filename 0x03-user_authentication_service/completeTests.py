#!/usr/bin/env python3
"""End-to-end integration test
"""
from auth import Auth
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """assert correct response to register user with email and password"""
    response = requests.post('http://127.0.0.1:5000/users', data={
        'email': email,
        'password': password
    })

    if response.status_code == 200:
        assert (response.json() == {"email": email, "message": "user created"})
    else:
        assert (response.status_code == 400)
        assert (response.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """ assert correct response to register user with
        email and incorrect password."""
    response = requests.post('http://127.0.0.1:5000/sessions', data={
        'email': email,
        'password': password
    })

    assert (response.status_code == 401)


def profile_unlogged() -> None:
    """ assert correct response to the
        profile endpoint without logging in: 403."""
    response = requests.get('http://127.0.0.1:5000/profile')
    assert (response.status_code == 403)


def log_in(email: str, password: str) -> str:
    """
    assert correct response to
    logging email and password
    returns session ID"""
    response = requests.post('http://127.0.0.1:5000/sessions', data={
        'email': email,
        'password': password
    })

    if response.status_code == 200:
        assert (response.json() == {"email": email, "message": "logged in"})
        return response.cookies.get('session_id')
    else:
        assert (response.status_code == 401)


def profile_logged(session_id: str) -> None:
    """
    assert correct response to the profile endpoint
    with a valid session ID.
    """
    cookies = {'session_id': session_id}
    response = requests.get('http://127.0.0.1:5000/profile', cookies=cookies)
    assert (response.status_code == 200)


def log_out(session_id: str) -> None:
    """
    assert correct response to the log out user
    with a specified session ID.
    """
    cookies = {'session_id': session_id}
    r = requests.delete('http://127.0.0.1:5000/sessions',
                        cookies=cookies)
    if r.status_code == 302:
        assert (r.url == 'http://127.0.0.1:5000/')
    else:
        assert (r.status_code == 200)


def reset_password_token(email: str) -> str:
    """
    assert correct response to
    Requests a password reset token for the specified email.
    """
    r = requests.post('http://127.0.0.1:5000/reset_password',
                      data={'email': email})
    if r.status_code == 200:
        token = r.json().get('reset_token')
        assert (r.json() == {"email": email, "reset_token": token})
    else:
        assert (r.status_code == 403)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    assert correct response to
    update the password for user email
    """
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    r = requests.put('http://127.0.0.1:5000/reset_password',
                     data=data)
    if r.status_code == 200:
        assert (r.json() == {"email": email, "message": "Password updated"})
    else:
        assert (r.status_code == 403)


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
