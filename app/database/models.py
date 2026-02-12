import uuid
from sqlalchemy import BigInteger, Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.database.base import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = Column(BigInteger, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())