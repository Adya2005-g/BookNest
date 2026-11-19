
from flask import Blueprint, request, jsonify

from database import db
from models.user import User
from models.notification import Notification

notification_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/api/notifications"
)


# CREATE NOTIFICATION
@notification_bp.route("/", methods=["POST"])
def create_notification():

    data = request.get_json() or {}

    user_id = data.get("user_id")
    message = data.get("message")

    if not user_id or not message:
        return jsonify({
            "message": "User ID and message are required"
        }), 400

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    notification = Notification(
        user_id=user_id,
        message=message
    )

    db.session.add(notification)
    db.session.commit()

    return jsonify({
        "message": "Notification created successfully!",
        "notification": notification.to_dict()
    }), 201


# GET USER NOTIFICATIONS
@notification_bp.route("/user/<int:user_id>", methods=["GET"])
def get_notifications(user_id):

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    notifications = Notification.query.filter_by(
        user_id=user_id
    ).order_by(Notification.created_at.desc()).all()

    return jsonify({
        "notifications": [
            notification.to_dict()
            for notification in notifications
        ]
    }), 200


# MARK NOTIFICATION AS READ
@notification_bp.route("/<int:notification_id>/read", methods=["PUT"])
def mark_as_read(notification_id):

    notification = db.session.get(
        Notification, notification_id
    )

    if not notification:
        return jsonify({
            "message": "Notification not found"
        }), 404

    notification.is_read = True
    db.session.commit()

    return jsonify({
        "message": "Notification marked as read!",
        "notification": notification.to_dict()
    }), 200
