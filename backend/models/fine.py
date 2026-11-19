
from database import db
from datetime import datetime

class Fine(db.Model):
    __tablename__ = "fines"

    id = db.Column(db.Integer, primary_key=True)

    issue_id = db.Column(
        db.Integer,
        db.ForeignKey("book_issues.id"),
        nullable=False
    )

    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="unpaid"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    issue = db.relationship("BookIssue")

    def to_dict(self):
        return {
            "id": self.id,
            "issue_id": self.issue_id,
            "amount": float(self.amount),
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
