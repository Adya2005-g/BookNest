
from flask import Blueprint, request, jsonify
from database import db
from models.book import Book
from models.category import Category

book_bp = Blueprint(
    "books",
    __name__,
    url_prefix="/api/books"
)


# GET ALL BOOKS
@book_bp.route("/", methods=["GET"])
def get_books():

    books = Book.query.all()

    return jsonify({
        "books": [book.to_dict() for book in books]
    }), 200


# ADD NEW BOOK
@book_bp.route("/", methods=["POST"])
def add_book():

    data = request.get_json() or {}

    required_fields = ["title", "author", "isbn", "category_id"]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "message": f"{field} is required"
            }), 400

    category = db.session.get(Category, data["category_id"])

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    if Book.query.filter_by(isbn=data["isbn"]).first():
        return jsonify({
            "message": "ISBN already exists"
        }), 409

    total_copies = data.get("total_copies", 1)

    if not isinstance(total_copies, int) or isinstance(total_copies, bool) or total_copies < 1:
        return jsonify({
            "message": "Total copies must be a positive integer"
        }), 400

    new_book = Book(
        title=data["title"],
        author=data["author"],
        isbn=data["isbn"],
        publisher=data.get("publisher"),
        description=data.get("description"),
        cover_image=data.get("cover_image"),
        category_id=data["category_id"],
        total_copies=total_copies,
        available_copies=total_copies
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        "message": "Book added successfully!",
        "book": new_book.to_dict()
    }), 201


# GET BOOK BY ID
@book_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):

    book = db.session.get(Book, book_id)

    if not book:
        return jsonify({
            "message": "Book not found"
        }), 404

    return jsonify({
        "book": book.to_dict()
    }), 200


# SEARCH BOOKS
@book_bp.route("/search", methods=["GET"])
def search_books():

    search_query = request.args.get("q", "").strip()

    if not search_query:
        return jsonify({
            "message": "Please provide a search term using ?q="
        }), 400

    books = Book.query.filter(
        db.or_(
            Book.title.ilike(f"%{search_query}%"),
            Book.author.ilike(f"%{search_query}%")
        )
    ).all()

    return jsonify({
        "books": [book.to_dict() for book in books]
    }), 200


# UPDATE BOOK
@book_bp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id):

    book = db.session.get(Book, book_id)

    if not book:
        return jsonify({
            "message": "Book not found"
        }), 404

    data = request.get_json() or {}

    if "isbn" in data:
        if not data["isbn"]:
            return jsonify({
                "message": "ISBN cannot be empty"
            }), 400

        existing = Book.query.filter(
            Book.isbn == data["isbn"],
            Book.id != book_id
        ).first()

        if existing:
            return jsonify({
                "message": "ISBN already exists"
            }), 409

    if "category_id" in data:
        category = db.session.get(Category, data["category_id"])
        if not category:
            return jsonify({
                "message": "Category not found"
            }), 404
        book.category_id = data["category_id"]

    for field in ["title", "author", "isbn", "publisher",
                  "description", "cover_image"]:
        if field in data:
            setattr(book, field, data[field])

    if "total_copies" in data:
        new_total = data["total_copies"]

        if not isinstance(new_total, int) or isinstance(new_total, bool) or new_total < 1:
            return jsonify({
                "message": "Total copies must be a positive integer"
            }), 400

        issued_copies = book.total_copies - book.available_copies

        if new_total < issued_copies:
            return jsonify({
                "message": "Total copies cannot be less than currently issued copies"
            }), 400

        book.total_copies = new_total
        book.available_copies = new_total - issued_copies

    db.session.commit()

    return jsonify({
        "message": "Book updated successfully!",
        "book": book.to_dict()
    }), 200


# DELETE BOOK
@book_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):

    book = db.session.get(Book, book_id)

    if not book:
        return jsonify({
            "message": "Book not found"
        }), 404

    if book.total_copies != book.available_copies:
        return jsonify({
            "message": "Cannot delete a book while copies are issued"
        }), 409

    db.session.delete(book)
    db.session.commit()

    return jsonify({
        "message": "Book deleted successfully!"
    }), 200
