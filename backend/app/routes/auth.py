from flask import Blueprint, request, jsonify
import bcrypt
from app.config.database import get_connection
import uuid
from werkzeug.utils import secure_filename
import os
from flask_jwt_extended import create_access_token
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

UPLOAD_FOLDER = os.path.join(
    os.getcwd(),
    "app",
    "uploads",
    "profile_photos"
)
ALLOWED_RESUME_EXTENSIONS = {"pdf"}

RESUME_UPLOAD_FOLDER = os.path.join(
    os.getcwd(),
    "app",
    "uploads",
    "resumes"
)

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

            access_token = create_access_token(
                identity=str(user[0]),
                additional_claims={
                    "name": user[1],
                    "email": user[2]
                }
            )

            return jsonify({
                "message": "Login successful",
                "access_token": access_token,
                "user": {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2]
                }
            }), 200

        else:
            return jsonify({
                "message": "Invalid email or password"
            }), 401

    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500

def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@auth.route("/upload/photo", methods=["POST"])
@jwt_required()
def upload_photo():

    # Check if a file was uploaded
    if "photo" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["photo"]

    # Get email from form-data
    user_id = get_jwt_identity()

    # Check if filename is empty
    if file.filename == "":
        return jsonify({"message": "No file selected"}), 400

    # Validate file extension
    if not allowed_file(file.filename):
        return jsonify({
            "message": "Only PNG, JPG and JPEG files are allowed"
        }), 400

    # Create a safe filename
    filename = secure_filename(file.filename)

    # Generate a unique filename
    unique_filename = f"{uuid.uuid4()}_{filename}"

    # Build full file path
    file_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )

    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Save file
    file.save(file_path)

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Update database
        cur.execute(
            """
            UPDATE users
            SET profile_photo = %s
            WHERE id = %s
            """,
            (
                f"uploads/profile_photos/{unique_filename}",
                user_id
            )
        )

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "message": "Profile photo uploaded successfully",
            "filename": unique_filename
        }), 200

    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500

def allowed_resume(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_RESUME_EXTENSIONS
    )

@auth.route("/upload/resume", methods=["POST"])
@jwt_required()
def upload_resume():

    if "resume" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["resume"]

    user_id = get_jwt_identity()

    if file.filename == "":
        return jsonify({"message": "No file selected"}), 400

    if not allowed_resume(file.filename):
        return jsonify({"message": "Only PDF files are allowed"}), 400

    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"

    os.makedirs(RESUME_UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(
        RESUME_UPLOAD_FOLDER,
        unique_filename
    )

    file.save(file_path)

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE users
            SET resume_file = %s
            WHERE id = %s
            """,
            (
                f"uploads/resumes/{unique_filename}",
                user_id
            )
        )

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "message": "Resume uploaded successfully",
            "filename": unique_filename
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500