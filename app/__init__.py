from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from .model import db
from .routes import routes

load_dotenv()

jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    print("🚀 Starting Flask App...")

    # Config
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "mysecretkey")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwtsecretkey")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600 * 24
    app.config["JWT_VERIFY_SUB"] = False
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init extensions
    db.init_app(app)
    CORS(app)
    jwt.init_app(app)

    # Register routes
    app.register_blueprint(routes)

    # 🔥 DB TABLE CREATION + DEBUG
    with app.app_context():
        try:
            print("📦 Importing models...")

            from .model import (
                User, Resume, Experience, Education,
                Project, Achievement, Language, Hobby
            )

            print("🛠 Creating database tables...")
            db.create_all()

            print("🔍 Checking created tables...")

            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()

            print("✅ Tables in DB:", tables)

            expected_tables = [
                "users", "resumes", "experiences", "educations",
                "projects", "achievements", "languages", "hobbies"
            ]

            missing = [t for t in expected_tables if t not in tables]

            if missing:
                print("❌ Missing tables:", missing)
            else:
                print("🎉 All tables created successfully!")

            print("📁 DB Location:", os.path.abspath("resume.db"))

        except Exception as e:
            print("🔥 ERROR while creating tables:")
            print(str(e))

    return app