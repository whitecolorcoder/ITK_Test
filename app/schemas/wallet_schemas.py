from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

class WalletOperationRequest(BaseModel):
    operation_type: OperationType
    amount: int = Field(gt=0)

class WalletResponse(BaseModel):
    wallet_id: UUID
    balance: int
