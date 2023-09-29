from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Newsletter(db.Model, SerializerMixin):
    __tablename__ = 'newsletters'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    published_at = db.Column(db.DateTime, server_default=db.func.now())
    edited_at = db.Column(db.DateTime, onupdate=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "published_at": str(self.published_at),
            "edited_at": str(self.edited_at) if self.edited_at else None,
        }
