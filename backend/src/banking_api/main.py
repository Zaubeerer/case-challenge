from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_db_and_tables
from .routes import accounts, customers, transfers


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(transfers.router, prefix="/transfers", tags=["transfers"])
