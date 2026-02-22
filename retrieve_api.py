import sqlite3
from flask import Flask, jsonify, request

from configmodule import config


app = Flask(__name__)


def _get_connection():
    return sqlite3.connect(str(config.SQLITE_DB_PATH))


def _discover_text_columns(connection):
    candidates = []
    cursor = connection.cursor()
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

    for (table_name,) in tables:
        pragma_rows = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
        text_columns = [row[1] for row in pragma_rows if str(row[2]).upper() in {"TEXT", ""}]
        if text_columns:
            candidates.append((table_name, text_columns))

    return candidates


def _search_sqlite(query_text, top_k=5):
    if not query_text:
        return []

    try:
        with _get_connection() as connection:
            candidates = _discover_text_columns(connection)
            cursor = connection.cursor()
            pattern = f"%{query_text}%"
            results = []

            for table_name, text_columns in candidates:
                where_clause = " OR ".join([f"{column} LIKE ?" for column in text_columns])
                sql = f"SELECT rowid, * FROM {table_name} WHERE {where_clause} LIMIT ?"
                params = [pattern for _ in text_columns] + [top_k]

                try:
                    rows = cursor.execute(sql, params).fetchall()
                    if not rows:
                        continue

                    column_names = ["rowid"] + [description[0] for description in cursor.description[1:]]
                    for row in rows:
                        row_obj = dict(zip(column_names, row))
                        results.append({
                            "table": table_name,
                            "row": row_obj,
                        })
                        if len(results) >= top_k:
                            return results
                except sqlite3.Error:
                    continue

            return results
    except sqlite3.Error:
        return []


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "retrieve api running"}), 200


@app.route("/query", methods=["POST"])
def query():
    payload = request.get_json(silent=True) or {}
    query_text = payload.get("query", "")
    top_k = int(payload.get("top_k", 5))
    results = _search_sqlite(query_text, top_k=top_k)
    return jsonify({"results": results}), 200


@app.route("/retrieve", methods=["POST"])
def retrieve():
    return query()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)
