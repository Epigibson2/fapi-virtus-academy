import sys
import os
sys.path.append("/opt/python/lib/python3.12/site-packages")
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1.router import router
from core.config import settings
from dependencies.database import init_db
from docs import tags_metadata
from mangum import Mangum

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB.
    await init_db()
    print("Init db ...")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    root_path="/dev",
    description="API para la plataforma de Virtus Academy",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=tags_metadata,
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan
)

app.include_router(router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return JSONResponse(content=get_openapi(title="Mi API", version="1.0.0", routes=app.routes))

handler = Mangum(app)