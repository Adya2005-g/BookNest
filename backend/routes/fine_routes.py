
from flask import Blueprint, jsonify
from database import db
from models.fine import Fine
from models.user import User

fine_bp = Blueprint(
    "fines",
    __name__,
    url_prefix="/api/fines"
)


# GET ALL FINES
@fine_bp.route("/", methods=["GET"])
def get_all_fines():

    fines = Fine.query.order_by(
        Fine.created_at.desc()
    ).all()

    return jsonify({
        "fines": [fine.to_dict() for fine in fines]
    }), 200


# GET FINES FOR A PARTICULAR USER
@fine_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_fines(user_id):

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    fines = (
        Fine.query
        .join(Fine.issue)
        .filter_by(user_id=user_id)
        .order_by(Fine.created_at.desc())
        .all()
    )

    return jsonify({
        "fines": [fine.to_dict() for fine in fines]
    }), 200


# MARK FINE AS PAID
@fine_bp.route("/<int:fine_id>/pay", methods=["PUT"])
def pay_fine(fine_id):

    fine = db.session.get(Fine, fine_id)

    if not fine:
        return jsonify({
            "message": "Fine not found"
        }), 404

    if fine.status == "paid":
        return jsonify({
            "message": "Fine has already been paid"
        }), 409

    fine.status = "paid"
    db.session.commit()

    return jsonify({
        "message": "Fine paid successfully!",
        "fine": fine.to_dict()
    }), 200
