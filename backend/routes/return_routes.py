
from flask import Blueprint, jsonify
from datetime import date
from decimal import Decimal

from database import db
from models.book_issue import BookIssue
from models.book import Book
from models.fine import Fine

return_bp = Blueprint(
    "returns",
    __name__,
    url_prefix="/api/returns"
)

# Fine charged per late day (in rupees)
FINE_PER_DAY = Decimal("5.00")


# RETURN A BOOK
@return_bp.route("/<int:issue_id>", methods=["POST"])
def return_book(issue_id):

    issue = db.session.get(BookIssue, issue_id)

    if not issue:
        return jsonify({
            "message": "Issue record not found"
        }), 404

    if issue.status != "issued":
        return jsonify({
            "message": "This book has already been returned"
        }), 409

    book = db.session.get(Book, issue.book_id)

    if not book:
        return jsonify({
            "message": "Book not found"
        }), 404

    today = date.today()
    issue.return_date = today
    issue.status = "returned"

    book.available_copies += 1

    late_days = max(0, (today - issue.due_date).days)
    fine_amount = FINE_PER_DAY * late_days

    if fine_amount > 0:
        new_fine = Fine(
            issue_id=issue.id,
            amount=fine_amount,
            status="unpaid"
        )
        db.session.add(new_fine)

    db.session.commit()

    return jsonify({
        "message": "Book returned successfully!",
        "issue": issue.to_dict(),
        "late_days": late_days,
        "fine_amount": float(fine_amount),
        "fine_status": "unpaid" if fine_amount > 0 else "no fine"
    }), 200
