
from database import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    author = db.Column(
        db.String(150),
        nullable=False
    )

    isbn = db.Column(
        db.String(30),
        unique=True
    )

    publisher = db.Column(db.String(150))
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(255))

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=True
    )

    total_copies = db.Column(
        db.Integer,
        default=1
    )

    available_copies = db.Column(
        db.Integer,
        default=1
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publisher": self.publisher,
            "description": self.description,
            "cover_image": self.cover_image,
            "category_id": self.category_id,
            "category_name": (
                self.category.category_name
                if self.category else None
            ),
            "total_copies": self.total_copies,
            "available_copies": self.available_copies
        }
