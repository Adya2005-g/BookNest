
from flask import Blueprint, request, jsonify
from datetime import date, timedelta

from database import db
from models.book import Book
from models.user import User
from models.book_issue import BookIssue

issue_bp = Blueprint(
    "issues",
    __name__,
    url_prefix="/api/issues"
)


# ISSUE A BOOK
@issue_bp.route("/", methods=["POST"])
def issue_book():

    data = request.get_json() or {}

    user_id = data.get("user_id")
    book_id = data.get("book_id")

    if not user_id or not book_id:
        return jsonify({
            "message": "User ID and Book ID are required"
        }), 400

    user = db.session.get(User, user_id)
    book = db.session.get(Book, book_id)

    if not user or not user.is_active:
        return jsonify({
            "message": "Active user not found"
        }), 404

    if not book:
        return jsonify({
            "message": "Book not found"
        }), 404

    if book.available_copies <= 0:
        return jsonify({
            "message": "No copies available"
        }), 409

    existing_issue = BookIssue.query.filter_by(
        user_id=user_id,
        book_id=book_id,
        status="issued"
    ).first()

    if existing_issue:
        return jsonify({
            "message": "This user already has this book issued"
        }), 409

    issue_date = date.today()
    due_date = issue_date + timedelta(days=14)

    new_issue = BookIssue(
        user_id=user_id,
        book_id=book_id,
        issue_date=issue_date,
        due_date=due_date,
        status="issued"
    )

    book.available_copies -= 1

    db.session.add(new_issue)
    db.session.commit()

    return jsonify({
        "message": "Book issued successfully!",
        "issue": new_issue.to_dict()
    }), 201


# GET ALL ISSUED BOOKS
@issue_bp.route("/", methods=["GET"])
def get_issued_books():

    issues = BookIssue.query.order_by(
        BookIssue.issue_date.desc()
    ).all()

    return jsonify({
        "issues": [issue.to_dict() for issue in issues]
    }), 200


# GET ISSUES FOR A USER
@issue_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_issues(user_id):

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    issues = BookIssue.query.filter_by(
        user_id=user_id
    ).all()

    return jsonify({
        "issues": [issue.to_dict() for issue in issues]
    }), 200
