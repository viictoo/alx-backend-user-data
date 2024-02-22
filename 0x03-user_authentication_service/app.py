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
    """basepath: Logout user"""
    session_id = request.cookies.get('session_id')
    marehemu = AUTH.get_user_from_session_id(session_id=session_id)
    if marehemu:
        AUTH.destroy_session(marehemu.id)
        return redirect('/')
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
