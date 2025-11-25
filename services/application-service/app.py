import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, g


def create_app(database_path=None):
    """Flask service to manage job applications."""
    app = Flask(__name__)
    db_path = database_path or os.getenv("APPLICATION_DB", ":memory:")

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
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        db.commit()

    @app.before_first_request
    def startup():
        init_db()

    @app.route("/applications", methods=["POST"])
    def create_application():
        data = request.get_json() or {}
        user_id = data.get("user_id")
        job_id = data.get("job_id")
        status = data.get("status", "submitted")
        if not user_id or not job_id:
            return jsonify({"error": "user_id and job_id are required"}), 400
        db = get_db()
        created_at = datetime.utcnow().isoformat()
        db.execute(
            "INSERT INTO applications (user_id, job_id, status, created_at) VALUES (?, ?, ?, ?)",
            (user_id, job_id, status, created_at),
        )
        db.commit()
        application_id = db.execute(
            "SELECT last_insert_rowid() AS id"
        ).fetchone()["id"]
        return jsonify({"id": application_id, "user_id": user_id, "job_id": job_id, "status": status, "created_at": created_at}), 201

    @app.route("/applications", methods=["GET"])
    def list_applications():
        user_id = request.args.get("user_id")
        job_id = request.args.get("job_id")
        db = get_db()
        query = "SELECT id, user_id, job_id, status, created_at FROM applications"
        params = []
        conditions = []
        if user_id:
            conditions.append("user_id = ?")
            params.append(user_id)
        if job_id:
            conditions.append("job_id = ?")
            params.append(job_id)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY created_at DESC"
        rows = db.execute(query, tuple(params)).fetchall()
        return jsonify([dict(row) for row in rows])

    @app.route("/applications/<int:application_id>", methods=["GET"])
    def get_application(application_id):
        db = get_db()
        app_row = db.execute(
            "SELECT id, user_id, job_id, status, created_at FROM applications WHERE id = ?",
            (application_id,),
        ).fetchone()
        if app_row:
            return jsonify(dict(app_row))
        return jsonify({"error": "Application not found"}), 404

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "application-service up"})

    return app


if __name__ == "__main__":
    app = create_app(os.getenv("APPLICATION_DB", "/data/applications.db"))
    app.run(host="0.0.0.0", port=5003, debug=True)