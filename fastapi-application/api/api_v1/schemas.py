from pydantic import BaseModel, ConfigDict


class Currency(BaseModel):
    from_currency: str
    to_currency: str
    amount: int