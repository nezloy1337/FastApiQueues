from contextlib import asynccontextmanager
from core.models import db_helper
import uvicorn
from fastapi import FastAPI

from core.config import settings
from fastapi.responses import ORJSONResponse
from api.api_v1 import router as api_router

from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    # startapp
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


main_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Остальная часть вашего кода

main_app.include_router(api_router)








if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
