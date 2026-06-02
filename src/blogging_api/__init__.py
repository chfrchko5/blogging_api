from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
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
        createdAt = db.Column(db.TIMESTAMP, default=func.current_timestamp())
        updatedAt = db.Column(db.TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    with app.app_context():
        db.create_all()

    @app.route("/posts", methods=["GET", "POST", "PUT"])
    def posts():
        if request.method == 'POST':
            data = request.get_json()

            post = Blog(
                title = data["title"],
                content = data["content"],
                category = data["category"],
                tags = data["tags"]
            )

            db.session.add(post)
            db.session.commit()

            return jsonify({
                "id": post.id,
                "title": post.title
            }), 201
        
        if request.method == 'GET':
            blogs = Blog.query.all()
            
            return jsonify([{
                "id": b.id,
                "title": b.title,
                "content": b.content
            } for b in blogs
            ]), 200


    return app