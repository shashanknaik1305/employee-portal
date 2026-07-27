from flask import Flask
from app.config.database import get_connection

app = Flask(__name__)

@app.route("/")
def home():
    try:
        conn = get_connection()
        conn.close()
        return "Database Connected Successfully!"
    except Exception as e:
        return f"Database Connection Failed: {e}"

if __name__ == "__main__":
    app.run(debug=True)