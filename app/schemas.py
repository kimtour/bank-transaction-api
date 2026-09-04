from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AccountCreate(BaseModel):
    account_name: str = Field(min_length=2, max_length=120)
    opening_balance: Decimal = Field(default=Decimal("0.00"), ge=0)
    currency: str = Field(default="KES", min_length=3, max_length=3)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()


class AccountResponse(BaseModel):
    id: int
    account_number: str
    account_name: str
    balance: Decimal
    currency: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class MoneyRequest(BaseModel):
    amount: Decimal = Field(gt=0, decimal_places=2)
    reference: str = Field(min_length=4, max_length=64)
    description: str | None = Field(default=None, max_length=255)


class TransferRequest(MoneyRequest):
    source_account: str
    destination_account: str


class TransactionResponse(BaseModel):
    id: int
    reference: str
    transaction_type: str
    amount: Decimal
    source_account_id: int | None
    destination_account_id: int | None
    description: str | None
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
