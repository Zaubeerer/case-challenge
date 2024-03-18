from sqlmodel import Field, SQLModel


class Customer(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
