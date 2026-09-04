import random
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from .models import Account, Transaction, User


def generate_account_number(db: Session) -> str:
    while True:
        number = f"10{random.randint(10000000, 99999999)}"
        if db.scalar(select(Account).where(Account.account_number == number)) is None:
            return number


def get_owned_account(db: Session, account_number: str, user: User) -> Account:
    account = db.scalar(select(Account).where(Account.account_number == account_number, Account.owner_id == user.id))
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


def ensure_unique_reference(db: Session, reference: str) -> None:
    if db.scalar(select(Transaction).where(Transaction.reference == reference)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Transaction reference already exists")


def deposit(db: Session, account: Account, amount: Decimal, reference: str, description: str | None) -> Transaction:
    ensure_unique_reference(db, reference)
    account.balance = Decimal(account.balance) + amount
    tx = Transaction(reference=reference, transaction_type="DEPOSIT", amount=amount, destination_account_id=account.id, description=description)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def withdraw(db: Session, account: Account, amount: Decimal, reference: str, description: str | None) -> Transaction:
    ensure_unique_reference(db, reference)
    if Decimal(account.balance) < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    account.balance = Decimal(account.balance) - amount
    tx = Transaction(reference=reference, transaction_type="WITHDRAWAL", amount=amount, source_account_id=account.id, description=description)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def transfer(db: Session, source: Account, destination: Account, amount: Decimal, reference: str, description: str | None) -> Transaction:
    ensure_unique_reference(db, reference)
    if source.id == destination.id:
        raise HTTPException(status_code=400, detail="Source and destination accounts must differ")
    if source.currency != destination.currency:
        raise HTTPException(status_code=400, detail="Currency mismatch")
    if Decimal(source.balance) < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    source.balance = Decimal(source.balance) - amount
    destination.balance = Decimal(destination.balance) + amount
    tx = Transaction(reference=reference, transaction_type="TRANSFER", amount=amount, source_account_id=source.id, destination_account_id=destination.id, description=description)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def transaction_history(db: Session, account_ids: list[int]) -> list[Transaction]:
    if not account_ids:
        return []
    return list(db.scalars(select(Transaction).where(or_(Transaction.source_account_id.in_(account_ids), Transaction.destination_account_id.in_(account_ids))).order_by(Transaction.created_at.desc())))
