
from database import db

class BookLink(db.Model):
    __tablename__ = "book_links"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("books.id"),
        nullable=False
    )

    platform = db.Column(
        db.String(100),
        nullable=False
    )

    link_type = db.Column(
        db.String(30),
        nullable=False
    )

    purchase_url = db.Column(
        db.String(1000),
        nullable=False
    )

    format = db.Column(
        db.String(50)
    )

    book = db.relationship("Book")

    def to_dict(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "platform": self.platform,
            "link_type": self.link_type,
            "purchase_url": self.purchase_url,
            "format": self.format
        }
