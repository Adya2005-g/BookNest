
from flask import Blueprint, jsonify

from models.book import Book
from models.user import User
from models.book_issue import BookIssue
from models.reservation import Reservation
from models.fine import Fine

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard"
)


@dashboard_bp.route("/stats", methods=["GET"])
def get_dashboard_stats():

    total_books = Book.query.count()

    total_members = User.query.filter_by(
        role="member"
    ).count()

    issued_books = BookIssue.query.filter_by(
        status="issued"
    ).count()

    returned_books = BookIssue.query.filter_by(
        status="returned"
    ).count()

    pending_reservations = Reservation.query.filter_by(
        status="pending"
    ).count()

    unpaid_fines = Fine.query.filter_by(
        status="unpaid"
    ).count()

    return jsonify({
        "total_books": total_books,
        "total_members": total_members,
        "issued_books": issued_books,
        "returned_books": returned_books,
        "pending_reservations": pending_reservations,
        "unpaid_fines": unpaid_fines
    }), 200
