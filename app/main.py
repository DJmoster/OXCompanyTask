import uvicorn

from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.config import settings
from app.database.utils import DatabaseUtils
from app.api_v1 import router as api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    DatabaseUtils.create_tables()
    DatabaseUtils.create_basic_admin()

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_v1_router, prefix=settings.api_v1_prefix)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app")
