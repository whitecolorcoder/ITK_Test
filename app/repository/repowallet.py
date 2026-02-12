from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.models import Wallet
from app.exception.exception import WalletNotFound


class WalletRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, wallet_id: UUID) -> Wallet:
        wallet = self.session.get(Wallet, wallet_id)

        if not wallet:
            raise WalletNotFound()

        return wallet

    def get_for_update(self, wallet_id: UUID) -> Wallet:
        result = self.session.execute(
            select(Wallet)
            .where(Wallet.id == wallet_id)
            .with_for_update()
        )
        wallet = result.scalar_one_or_none()

        if not wallet:
            raise WalletNotFound()

        return wallet

    def commit(self):
        self.session.commit()



