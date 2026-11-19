
from flask import Blueprint, request, jsonify
from datetime import datetime

from database import db
from models.user import User
from models.book import Book
from models.reservation import Reservation

reservation_bp = Blueprint(
    "reservations",
    __name__,
    url_prefix="/api/reservations"
)


# CREATE RESERVATION
@reservation_bp.route("/", methods=["POST"])
def create_reservation():

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

    existing = Reservation.query.filter_by(
        user_id=user_id,
        book_id=book_id,
        status="pending"
    ).first()

    if existing:
        return jsonify({
            "message": "You already have a pending reservation"
        }), 409

    new_reservation = Reservation(
        user_id=user_id,
        book_id=book_id,
        reservation_date=datetime.utcnow(),
        status="pending"
    )

    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({
        "message": "Book reserved successfully!",
        "reservation": new_reservation.to_dict()
    }), 201


# GET ALL RESERVATIONS
@reservation_bp.route("/", methods=["GET"])
def get_reservations():

    reservations = Reservation.query.order_by(
        Reservation.reservation_date.desc()
    ).all()

    return jsonify({
        "reservations": [
            reservation.to_dict()
            for reservation in reservations
        ]
    }), 200


# GET USER RESERVATIONS
@reservation_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_reservations(user_id):

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    reservations = Reservation.query.filter_by(
        user_id=user_id
    ).all()

    return jsonify({
        "reservations": [
            reservation.to_dict()
            for reservation in reservations
        ]
    }), 200
