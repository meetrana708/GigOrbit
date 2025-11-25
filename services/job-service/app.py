import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, g


def create_app(database_path=None):
    """Create a Flask application for job postings."""
    app = Flask(__name__)
    db_path = database_path or os.getenv("JOB_DB", ":memory:")

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
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                company TEXT,
                location TEXT,
                created_at TEXT NOT NULL
            );
            """
        )
        db.commit()

    @app.before_first_request
    def startup():
        init_db()

    @app.route("/jobs", methods=["POST"])
    def create_job():
        data = request.get_json() or {}
        title = data.get("title")
        description = data.get("description")
        company = data.get("company")
        location = data.get("location")
        if not title:
            return jsonify({"error": "Title is required"}), 400
        db = get_db()
        created_at = datetime.utcnow().isoformat()
        db.execute(
            "INSERT INTO jobs (title, description, company, location, created_at) VALUES (?, ?, ?, ?, ?)",
            (title, description, company, location, created_at),
        )
        db.commit()
        job_id = db.execute(
            "SELECT last_insert_rowid() AS id"
        ).fetchone()["id"]
        return jsonify({"id": job_id, "title": title, "description": description, "company": company, "location": location, "created_at": created_at}), 201

    @app.route("/jobs", methods=["GET"])
    def list_jobs():
        db = get_db()
        jobs = db.execute(
            "SELECT id, title, description, company, location, created_at FROM jobs ORDER BY created_at DESC"
        ).fetchall()
        return jsonify([dict(job) for job in jobs])

    @app.route("/jobs/<int:job_id>", methods=["GET"])
    def get_job(job_id):
        db = get_db()
        job = db.execute(
            "SELECT id, title, description, company, location, created_at FROM jobs WHERE id = ?",
            (job_id,),
        ).fetchone()
        if job:
            return jsonify(dict(job))
        return jsonify({"error": "Job not found"}), 404

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "job-service up"})

    return app


if __name__ == "__main__":
    app = create_app(os.getenv("JOB_DB", "/data/jobs.db"))
    app.run(host="0.0.0.0", port=5002, debug=True)