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

@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    try:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, name, email, password_hash
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user is None:
            return jsonify({"message": "Invalid email or password"}), 401

        stored_password_hash = user[3]

        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password_hash.encode("utf-8")
        ):

            return jsonify({
                "message": "Login successful",
                "user": {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2]
                }
            }), 200

        return jsonify({"message": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"message": str(e)}), 500