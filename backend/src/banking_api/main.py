from fastapi import FastAPI

from .routes import accounts, customers, transfers

app = FastAPI()

app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(transfers.router, prefix="/transfers", tags=["transfers"])
