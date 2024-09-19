#!/usr/bin/env python3
"""
    Module implementing all routes for session authentication

"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login/', methods=['POST'],
                 strict_slashes=False)
def auth_session_login():
    """Implements all routes for session authentication"""
    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})

    if not user:
        return jsonify({"error": "no user found for this email"}), 400

    user = user[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)

    response = jsonify(user.to_json())

    session_name = os.getenv("SESSION_NAME")

    response.set_cookie(session_name, session_id)

    return response


@app_views.route('/auth_session/logout/', methods=["DELETE"],
                 strict_slashes=False)
def auth_session_logout():
    """Handles user logout from current session"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
