from routes.dashboard_routes import dashboard_bp
from routes.notification_routes import notification_bp
from routes.wishlist_routes import wishlist_bp
from routes.fine_routes import fine_bp
from routes.reservation_routes import reservation_bp
from routes.return_routes import return_bp
from routes.issue_routes import issue_bp
from routes.book_routes import book_bp
from routes.category_routes import category_bp
from routes.auth_routes import auth_bp
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database import db

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173"]
        }
    })

    db.init_app(app)

    import models

    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(issue_bp)
    app.register_blueprint(return_bp)
    app.register_blueprint(reservation_bp)
    app.register_blueprint(fine_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(dashboard_bp)

    @app.route("/")
    def home():
        return jsonify({
            "message": "Welcome to BookNest Library Management System",
            "status": "Running"
        })

    @app.route("/api/health")
    def health():
        return jsonify({
            "status": "healthy"
        })

    @app.route("/api/db-check")
    def database_check():
        try:
            from sqlalchemy import text
            db.session.execute(text("SELECT 1"))

            return jsonify({
                "message": "MySQL connected successfully!",
                "database": "booknest_db"
            })

        except Exception as e:
            return jsonify({
                "message": "Database connection failed",
                "error": str(e)
            }), 500

    return app


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

    app.run(debug=True, port=5000)