import uuid
from app.web.db import db
from .base import BaseModel


class Conversation(BaseModel):
    id: str = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    memory: str = db.Column(db.String)
    llm: str = db.Column(db.String)

    user_id: int = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="conversations")

    messages = db.relationship(
        "Message", back_populates="conversation", order_by="Message.created_on"
    )

    def as_dict(self):
        return {
            "id": self.id,
            "messages": [m.as_dict() for m in self.messages],
        }
