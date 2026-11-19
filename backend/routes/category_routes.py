
from flask import Blueprint, request, jsonify
from database import db
from models.category import Category

category_bp = Blueprint(
    "categories",
    __name__,
    url_prefix="/api/categories"
)


# GET ALL CATEGORIES
@category_bp.route("/", methods=["GET"])
def get_categories():

    categories = Category.query.all()

    return jsonify({
        "categories": [category.to_dict() for category in categories]
    }), 200


# ADD NEW CATEGORY
@category_bp.route("/", methods=["POST"])
def add_category():

    data = request.get_json() or {}

    category_name = data.get("category_name")
    description = data.get("description")

    if not category_name:
        return jsonify({
            "message": "Category name is required"
        }), 400

    existing_category = Category.query.filter_by(
        category_name=category_name
    ).first()

    if existing_category:
        return jsonify({
            "message": "Category already exists"
        }), 409

    new_category = Category(
        category_name=category_name,
        description=description
    )

    db.session.add(new_category)
    db.session.commit()

    return jsonify({
        "message": "Category added successfully!",
        "category": new_category.to_dict()
    }), 201


# GET CATEGORY BY ID
@category_bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id):

    category = db.session.get(Category, category_id)

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    return jsonify({
        "category": category.to_dict()
    }), 200


# DELETE CATEGORY
@category_bp.route("/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):

    category = db.session.get(Category, category_id)

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    if category.books:
        return jsonify({
            "message": "Cannot delete category because books are assigned to it"
        }), 409

    db.session.delete(category)
    db.session.commit()

    return jsonify({
        "message": "Category deleted successfully!"
    }), 200
