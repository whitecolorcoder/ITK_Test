from uuid import UUID
from app.repository.repowallet import WalletRepository
from app.schemas.wallet_schemas import OperationType
from app.exception.exception import InsufficientFunds


class WalletService:
    def __init__(self, repo: WalletRepository):
        self.repo = repo

    def operate(
        self,
        wallet_id: UUID,
        operation_type: OperationType,
        amount: int
    ):
        wallet = self.repo.get_for_update(wallet_id)

        if operation_type == OperationType.DEPOSIT:
            wallet.balance += amount

        elif operation_type == OperationType.WITHDRAW:
            if wallet.balance < amount:
                raise InsufficientFunds()
            wallet.balance -= amount

        self.repo.commit()

        return wallet

    def get(self, wallet_id: UUID):
        return self.repo.get_by_id(wallet_id)
