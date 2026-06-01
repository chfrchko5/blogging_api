from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


def create_app():
    load_dotenv()
    DB_NAME = os.getenv("db_name")
    DB_USER = os.getenv("db_user")
    DB_PASS = os.getenv("db_pass")
    URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@localhost:3306/{DB_NAME}"

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = URI
    db = SQLAlchemy(app)

    class Blog(db.Model):
        __tablename__ = 'blog'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        title = db.Column(db.String(30), nullable=False)
        content = db.Column(db.Text, nullable=False)
        category = db.Column(db.String(20), nullable=False)
        tags = db.Column(db.Text, nullable=False)

        # DO THESE TWO AFTER SUCCESSFUL TABLE CREATION
        # createdAt = db.Column(db.TIMESTAMP)
        # updatedAt = db.Column(db.TIMESTAMP)

    with app.app_context():
        db.create_all()

    return app