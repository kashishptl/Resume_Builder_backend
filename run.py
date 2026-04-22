from app import create_app
from flask_cors import CORS
from app.model import db

app = create_app()

CORS(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True) 