from fastapi import APIRouter, Depends
from uuid import UUID
from app.schemas.wallet_schemas import WalletOperationRequest, WalletResponse
from app.services.wallet_service import WalletService

import app.dependecies.walletdep as walletdep


router = APIRouter(prefix="/wallets", tags=["Wallets"])


def _get_wallet_service():
    return walletdep.get_wallet_service()


@router.post("/{wallet_id}/operation", response_model=WalletResponse)
def operate_wallet(
    wallet_id: UUID,
    payload: WalletOperationRequest,
    service: WalletService = Depends(_get_wallet_service),
):
    wallet = service.operate(
        wallet_id,
        payload.operation_type,
        payload.amount,
    )

    return WalletResponse(wallet_id=wallet.id, balance=wallet.balance)


@router.get("/{wallet_id}", response_model=WalletResponse)
def get_wallet(wallet_id: UUID, service: WalletService = Depends(_get_wallet_service)):
    wallet = service.get(wallet_id)
    return WalletResponse(wallet_id=wallet.id, balance=wallet.balance)