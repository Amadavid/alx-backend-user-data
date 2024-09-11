#!/usr/bin/env python3
"""
    Module implementing a password-hashing function

"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and returns a salted hashed password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if provided password is valid"""
    return bcrypt.checkpw(password.encode(), hashed_password)
