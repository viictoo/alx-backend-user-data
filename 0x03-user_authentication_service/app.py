#!/usr/bin/env python3
"""Basic Flask App Module"""

from flask import Flask, jsonify, request, abort, redirect

from auth import Auth


app = Flask(__name__)
app.url_map.strict_slashes = False

AUTH = Auth()


@app.route('/')
def hello():
    """basepath: hello route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """basepath: register new user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"}), 200


@app.route('/sessions', methods=['POST'])
def login():
    """basepath: login user"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp, 200


@app.route('/sessions', methods=['DELETE'])
def logout():
    """basepath: DELETE user session"""
    session_id = request.cookies.get('session_id')
    marehemu = AUTH.get_user_from_session_id(session_id=session_id)
    if marehemu:
        AUTH.destroy_session(marehemu.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """
    request is expected to contain a session_id cookie.
    Use it to find the user. If the user exist, respond
    with a 200 HTTP status and a JSON payload:
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user:
        return jsonify({"email": user.email})
    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    request is expected to contain a session_id cookie.
    Use it to find the user. If the user exist, respond
    with a 200 HTTP status and a JSON payload:
    """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify(
        {"email": email, "reset_token": token}
        ), 200


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    The request is expected to contain form data with fields
    "email", "reset_token" and "new_password".
    Update the password. If the token is invalid, catch the exception
    and respond with a 403 HTTP code.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
