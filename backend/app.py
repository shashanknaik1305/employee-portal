from flask import Flask
from app.routes.auth import auth

app = Flask(__name__)

app.register_blueprint(auth)

@app.route("/")
def home():
    return "Employee Portal Backend Running"

if __name__ == "__main__":
    app.run(debug=True)