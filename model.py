from sqlalchemy import Integer, String, Boolean, Numeric, func, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
from datetime import datetime, timezone
from decimal import Decimal
import os
import secrets
from cryptography.fernet import Fernet, InvalidToken
from extensions import db
from flask import current_app


def get_fernet():
    """Get Fernet instance with key from config"""
    fernet_key = current_app.config.get('FERNET_KEY')
    if not fernet_key:
        raise RuntimeError("FERNET_KEY not configured")
    return Fernet(fernet_key.encode())

class Cafe(db.Model):
    __tablename__ = 'cafes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    map_url: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    country: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="cafes")

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100))

    api_key_enc: Mapped[str] = mapped_column(String(500), nullable=True)
    api_key_last4: Mapped[str] = mapped_column(String(10), nullable=True)
    api_key_created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    api_key_active: Mapped[bool] = mapped_column(Boolean, default=False)

    cafes = relationship("Cafe", back_populates="user")


def generate_raw_api_key():
    return secrets.token_urlsafe(32)

def encrypt_key(raw_key: str) -> str:
    fernet = get_fernet()
    return fernet.encrypt(raw_key.encode()).decode()

def decrypt_key(stored: str) -> str:
    fernet = get_fernet()
    try:
        return fernet.decrypt(stored.encode()).decode()
    except InvalidToken:
        raise RuntimeError("Stored API key could not be decrypted")

def create_and_store_api_key_for_user(user: User) -> str:
    while True:
        raw = generate_raw_api_key()
        last4 = raw[-4:]
        candidates = db.session.execute(
            db.select(User).filter_by(api_key_last4=last4, api_key_active=True)
        ).scalars().all()

        conflict = False
        for c in candidates:
            try:
                if decrypt_key(c.api_key_enc) == raw:
                    conflict = True
                    break
            except Exception:
                continue
        if not conflict:
            break

    enc = encrypt_key(raw)
    user.api_key_enc = enc
    user.api_key_last4 = raw[-4:]
    user.api_key_created_at = datetime.now(timezone.utc)
    user.api_key_active = True
    db.session.add(user)
    db.session.commit()
    return raw