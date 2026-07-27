from flask import Flask
from flask_cors import CORS 
from app.routes.auth import auth

app = Flask(__name__)
CORS(app)
app.register_blueprint(auth)

@app.route("/")
def home():
    return "Employee Portal Backend Running"

if __name__ == "__main__":
    app.run(debug=True)