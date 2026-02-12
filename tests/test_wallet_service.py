from fastapi.testclient import TestClient
from uuid import uuid4
from unittest.mock import MagicMock
import pytest

from main import app
from app.schemas.wallet_schemas import OperationType

client = TestClient(app)

@pytest.fixture
def fake_wallet_service(monkeypatch):
    """Мокаем WalletService для роутеров"""
    class FakeWallet:
        def __init__(self, wallet_id, balance):
            self.id = wallet_id
            self.balance = balance

    service_mock = MagicMock()

    
    def get_wallet(wallet_id):
        if wallet_id == uuid4(): 
            return None
        return FakeWallet(wallet_id, 100)
    service_mock.get = get_wallet

   
    def operate(wallet_id, operation_type, amount):
        balance = 100
        if operation_type == OperationType.DEPOSIT:
            balance += amount
        elif operation_type == OperationType.WITHDRAW:
            if amount > balance:
                raise ValueError("Insufficient funds")
            balance -= amount
        return FakeWallet(wallet_id, balance)
    service_mock.operate = operate

    monkeypatch.setattr("app.dependecies.walletdep.get_wallet_service", lambda: service_mock)
    return service_mock


def test_get_wallet(fake_wallet_service):
    wallet_id = uuid4()
    response = client.get(f"/wallets/{wallet_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert "balance" in data
    assert "wallet_id" in data


def test_post_deposit(fake_wallet_service):
    wallet_id = uuid4()
    payload = {"operation_type": "DEPOSIT", "amount": 50}
    response = client.post(f"/wallets/{wallet_id}/operation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == 150


def test_post_withdraw(fake_wallet_service):
    wallet_id = uuid4()
    payload = {"operation_type": "WITHDRAW", "amount": 40}
    response = client.post(f"/wallets/{wallet_id}/operation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == 60


def test_post_withdraw_insufficient(fake_wallet_service):
    wallet_id = uuid4()
    payload = {"operation_type": "WITHDRAW", "amount": 200}  
    response = client.post(f"/wallets/{wallet_id}/operation", json=payload)
    assert response.status_code in (400, 500) 
