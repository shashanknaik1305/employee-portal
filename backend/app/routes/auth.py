from flask import Blueprint, request, jsonify
import bcrypt
from app.config.database import get_connection

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO users(name,email,password_hash)
            VALUES (%s,%s,%s)
            """,
            (name, email, password_hash)
        )

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500