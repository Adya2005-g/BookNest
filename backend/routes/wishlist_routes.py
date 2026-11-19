
from flask import Blueprint, request, jsonify

from database import db
from models.user import User
from models.book import Book
from models.wishlist import Wishlist

wishlist_bp = Blueprint(
    "wishlist",
    __name__,
    url_prefix="/api/wishlist"
)


# ADD BOOK TO WISHLIST
@wishlist_bp.route("/", methods=["POST"])
def add_to_wishlist():

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

    existing = Wishlist.query.filter_by(
        user_id=user_id,
        book_id=book_id
    ).first()

    if existing:
        return jsonify({
            "message": "Book is already in your wishlist"
        }), 409

    new_item = Wishlist(
        user_id=user_id,
        book_id=book_id
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        "message": "Book added to wishlist!",
        "wishlist": new_item.to_dict()
    }), 201


# GET USER WISHLIST
@wishlist_bp.route("/user/<int:user_id>", methods=["GET"])
def get_wishlist(user_id):

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    items = Wishlist.query.filter_by(
        user_id=user_id
    ).all()

    return jsonify({
        "wishlist": [item.to_dict() for item in items]
    }), 200


# REMOVE BOOK FROM WISHLIST
@wishlist_bp.route("/<int:wishlist_id>", methods=["DELETE"])
def remove_from_wishlist(wishlist_id):

    item = db.session.get(Wishlist, wishlist_id)

    if not item:
        return jsonify({
            "message": "Wishlist item not found"
        }), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        "message": "Book removed from wishlist!"
    }), 200
