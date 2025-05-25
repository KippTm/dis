"""User model for managing user authentication and data storage in a database."""

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from db import db


class User:
    """Represents a user in the system with methods for authentication and user management."""

    def __init__(self, username, user_id=None):
        self.user_id = user_id
        self.username = username
        self.password_hash = None

    def set_password(self, password):
        """Hashes the plain password and stores it in self.password_hash."""
        self.password_hash = generate_password_hash(password)

    def try_create_user(self):
        """
        Attempts to create a new user in the database with a hashed password.
        Returns True if successful, False if the user already exists or an error occurs.
        """
        if not self.password_hash:
            print(
                "Error: Password hash not set. Call set_password() before try_create_user()."
            )
            return False

        # Check if user already exists
        check_user_query = "SELECT username FROM Users WHERE username = :username"
        existing_user = db.session.execute(
            text(check_user_query), {"username": self.username}
        ).fetchone()
        if existing_user:
            return False  # User already exists

        insert_user_query = (
            "INSERT INTO Users (username, password) VALUES (:username, :password_hash)"
        )
        try:
            db.session.execute(
                text(insert_user_query),
                {
                    "username": self.username,
                    "password_hash": self.password_hash,
                },
            )
            db.session.commit()  # Commit the transaction
            return True
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback in case of any error
            print(f"Error creating user: {e}")
            print(f"Error creating user: {e}")
            return False

    @staticmethod
    def find_by_username(username):
        """
        Finds a user by their username.
        Loads the username and password hash from the database.
        The 'password' column in the database is assumed to store the hash.
        """

        query = "SELECT username, password FROM Users WHERE username = :username"
        result = db.session.execute(text(query), {"username": username}).fetchone()
        if result:
            user = User(username=result[0])
            user.password_hash = result[1]
            return user
        return None

    def check_password(self, password_to_check):
        """Checks the provided plain password against the stored hash."""
        if not self.password_hash:
            return False  # No stored hash to compare against
        return check_password_hash(self.password_hash, password_to_check)

    @staticmethod
    def authenticate(username, password):
        """Authenticates a user. Returns User object if valid, None otherwise."""
        user = User.find_by_username(username)
        if user and user.check_password(password):
            return user
        return None
