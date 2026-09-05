from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Account, User
from .schemas import AccountCreate, AccountResponse, LoginRequest, MoneyRequest, RegisterRequest, TokenResponse, TransactionResponse, TransferRequest
from .security import create_access_token, get_current_user, hash_password, verify_password
from .services import deposit, generate_account_number, get_owned_account, transaction_history, transfer, withdraw

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bank Transaction API",
    version="1.0.0",
    description="A secure banking API demonstrating account management, transfers, validation, testing and CI/CD.",
)

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=FileResponse, include_in_schema=False)
def home():
    return FileResponse(static_dir / "index.html")


@app.get("/walkthrough", response_class=FileResponse, include_in_schema=False)
def walkthrough():
    return FileResponse(static_dir / "walkthrough.html")


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "service": "bank-transaction-api", "version": "1.0.0"}


@app.post("/auth/register", status_code=status.HTTP_201_CREATED, tags=["Authentication"])
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.username == payload.username)):
        raise HTTPException(status_code=409, detail="Username already exists")
    user = User(username=payload.username, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}


@app.post("/auth/login", response_model=TokenResponse, tags=["Authentication"])
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == payload.username))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return TokenResponse(access_token=create_access_token(user.id))


@app.post("/accounts", response_model=AccountResponse, status_code=201, tags=["Accounts"])
def create_account(payload: AccountCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    account = Account(account_number=generate_account_number(db), account_name=payload.account_name, balance=payload.opening_balance, currency=payload.currency, owner_id=user.id)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@app.get("/accounts", response_model=list[AccountResponse], tags=["Accounts"])
def list_accounts(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return list(db.scalars(select(Account).where(Account.owner_id == user.id).order_by(Account.id)))


@app.get("/accounts/{account_number}", response_model=AccountResponse, tags=["Accounts"])
def get_account(account_number: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_owned_account(db, account_number, user)


@app.post("/accounts/{account_number}/deposit", response_model=TransactionResponse, tags=["Transactions"])
def make_deposit(account_number: str, payload: MoneyRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return deposit(db, get_owned_account(db, account_number, user), payload.amount, payload.reference, payload.description)


@app.post("/accounts/{account_number}/withdraw", response_model=TransactionResponse, tags=["Transactions"])
def make_withdrawal(account_number: str, payload: MoneyRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return withdraw(db, get_owned_account(db, account_number, user), payload.amount, payload.reference, payload.description)


@app.post("/transfers", response_model=TransactionResponse, tags=["Transactions"])
def make_transfer(payload: TransferRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    source = get_owned_account(db, payload.source_account, user)
    destination = db.scalar(select(Account).where(Account.account_number == payload.destination_account))
    if destination is None:
        raise HTTPException(status_code=404, detail="Destination account not found")
    return transfer(db, source, destination, payload.amount, payload.reference, payload.description)


@app.get("/transactions", response_model=list[TransactionResponse], tags=["Transactions"])
def transactions(limit: int = Query(default=50, ge=1, le=200), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    account_ids = list(db.scalars(select(Account.id).where(Account.owner_id == user.id)))
    return transaction_history(db, account_ids)[:limit]
