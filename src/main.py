from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)
