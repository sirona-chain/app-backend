import uuid
from app.web.db import db
from .base import BaseModel
from substrateinterface import Keypair


class User(BaseModel):
    id: str = db.Column(
        db.String(), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    email: str = db.Column(db.String(80), unique=True, nullable=False)
    polkadot_address: str = db.Column(db.String(80), unique=True, nullable=True)
    polkadot_private_key: str = db.Column(db.String(255), nullable=True)
    conversations = db.relationship("Conversation", back_populates="user")

    def as_dict(self):
        return {"id": self.id, "email": self.email, "polkadot_address": self.polkadot_address}

    @classmethod
    def create_with_wallet(cls, email):
        keypair = Keypair.create_from_mnemonic(Keypair.generate_mnemonic())
        user = cls.create(email=email, polkadot_address=keypair.ss58_address, polkadot_private_key=keypair.seed_hex)
        return user
