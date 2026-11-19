
from database import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)

    category_name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    description = db.Column(db.Text)

    books = db.relationship(
        "Book",
        backref="category",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "category_name": self.category_name,
            "description": self.description
        }
