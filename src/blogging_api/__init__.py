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

    @app.route("/posts", methods=["GET", "POST"])
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
  
            return f"Post successfully created, ID:{post.id}, titled '{post.title}'", 201
                 
        if request.method == 'GET':
            term = request.args.get("term")

            blogs = Blog.query

            if term:
                blogs = blogs.filter(
                    Blog.title.ilike(f"%{term}%") |
                    Blog.content.ilike(f"%{term}%") |
                    Blog.category.ilike(f"%{term}%")
                )
            
            posts = blogs.all()

            return jsonify([{
                "id": p.id,
                "title": p.title,
                "content": p.content,
                "category": p.category,
                "tags": p.tags,
                "createdAt": p.createdAt,
                "updatedAt": p.updatedAt
            } for p in posts
            ]), 200

        return jsonify(error="Method not allowed"), 405
    
    @app.route("/posts/<int:post_id>", methods=["GET", "PUT"])
    def update_post(post_id):
        post = Blog.query.get(post_id)
        if not post:
                return f"Post ID:{post_id} not found.", 404


        if request.method == "GET":
            return jsonify({
                "id": post.id,
                "title": post.title,
                "content": post.content
            }), 200
        
        if request.method == "PUT":
            data = request.get_json()

            post = Blog.query.get(post_id)
            
            post.title = data["title"]
            post.content = data["content"]

            db.session.commit()

            return f"Post ID:{post_id} updated successfully.", 200

        if request.method == "DELETE":
            db.session.delete(post)
            db.session.commit()

            return f"Post ID:{post_id} successfully deleted.", 204

        return jsonify(error="Method not allowed"), 405

    return app