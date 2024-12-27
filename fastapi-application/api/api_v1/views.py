from pathlib import Path
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from api.api_v1.schemas import Currency
from core.config import settings
from core.models import db_helper


template_path = Path(__file__).parent.parent.parent / "core" / "templates"
templates = Jinja2Templates(directory=template_path)


router = APIRouter(
    tags=["Converter"],
    prefix=settings.api.v1.prefix,
)


@router.get("/", response_class=JSONResponse)
async def get_form(request: Request):
    return {
    "success": True,
    "base": "USD",
    "date": "2024-06-01",
    "rates": {
        "EUR": 0.85,
        "RUB": 92.50
    }
}



@router.post("/")
def post_convertion(
    request: Request,
    from_currency: str = Form(...),
    to_currency: str = Form(...),
    amount: int = Form(...),
):
    try:
        curr = Currency(from_currency=from_currency, to_currency=to_currency, amount=amount)
    except ValidationError as e:
        return {"error": e.errors()}
    return curr



