from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.repository.repowallet import WalletRepository
from app.services.wallet_service import WalletService


def get_wallet_repo(db: Session = Depends(get_db)) -> WalletRepository:
    return WalletRepository(db)

def get_wallet_service(
    repo: WalletRepository = Depends(get_wallet_repo),
) -> WalletService:
    return WalletService(repo)
