import os
import sqlite3
from flask import Flask, request, jsonify, g


def create_app(database_path=None):
    """
    Create a Flask application for the user service.  The service manages
    user accounts and provides endpoints for registration, login and profile
    retrieval.  Each user has a unique ID, email and password.  In this
    simplified example passwords are stored in plain text – replace with a
    proper hash in a real system.
    """
    app = Flask(__name__)
    db_path = database_path or os.getenv("USER_DB", ":memory:")

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(db_path)
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(exception):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db():
        db = get_db()
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'candidate'
            );
            """
        )
        db.commit()

    @app.before_first_request
    def startup():
        init_db()

    @app.route("/users/register", methods=["POST"])
    def register_user():
        data = request.get_json() or {}
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "candidate")
        if not all([name, email, password]):
            return jsonify({"error": "Missing required fields"}), 400
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                (name, email, password, role),
            )
            db.commit()
        except sqlite3.IntegrityError:
            return jsonify({"error": "Email already registered"}), 409
        user_id = db.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()["id"]
        return jsonify({"id": user_id, "name": name, "email": email, "role": role}), 201

    @app.route("/users/login", methods=["POST"])
    def login_user():
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400
        db = get_db()
        user = db.execute(
            "SELECT id, name, email, password, role FROM users WHERE email = ?",
            (email,),
        ).fetchone()
        if user and user["password"] == password:
            # In a real system return a JWT or session token.
            return jsonify({"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]})
        return jsonify({"error": "Invalid credentials"}), 401

    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        db = get_db()
        user = db.execute(
            "SELECT id, name, email, role FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if user:
            return jsonify(dict(user))
        return jsonify({"error": "User not found"}), 404

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "user-service up"})

    return app


if __name__ == "__main__":
    # When running locally (not via Gunicorn), create the app and run it
    app = create_app(os.getenv("USER_DB", "/data/users.db"))
    app.run(host="0.0.0.0", port=5001, debug=True)