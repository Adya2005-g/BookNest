
from database import db
from datetime import date, datetime

class BookIssue(db.Model):
    __tablename__ = "book_issues"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    book_id = db.Column(
        db.Integer,
        db.ForeignKey("books.id"),
        nullable=False
    )

    issue_date = db.Column(
        db.Date,
        default=date.today,
        nullable=False
    )

    due_date = db.Column(
        db.Date,
        nullable=False
    )

    return_date = db.Column(db.Date)

    status = db.Column(
        db.String(20),
        default="issued"
    )

    user = db.relationship("User")
    book = db.relationship("Book")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "issue_date": self.issue_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "return_date": (
                self.return_date.isoformat()
                if self.return_date else None
            ),
            "status": self.status
        }
