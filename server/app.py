#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b"Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route("/clear")
def clear_session():
    session["page_views"] = 0
    return {"message": "200: Successfully cleared session data."}, 200


@app.route("/articles")
def index_articles():
    articles = Article.query.all()
    articles_list = [article.to_dict() for article in articles]
    return jsonify(articles_list)


@app.route("/articles/<int:id>")
def show_article(id):
    # Initialize page views if not set
    session["page_views"] = session.get("page_views", 0) + 1

    # Check if the user has viewed more than 3 pages
    if session["page_views"] > 3:
        return jsonify({"message": "Maximum pageview limit reached"}), 401

    # Fetch the article by ID
    selected = Article.query.filter_by(id=id).first()

    # Check if the article was found
    if selected is None:
        return jsonify({"error": "Article not found"}), 404

    # Return the article as JSON
    response = selected.to_dict()
    response["page_views"] = session["page_views"]

    return jsonify(response)


if __name__ == "__main__":
    app.run(port=5555)
