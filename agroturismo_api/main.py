from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import (
    API_PREFIX,
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    IS_DEBUG,
)
from .core.db import create_db_and_tables, engine
from .routes import main_router

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://agroturismo.vercel.app",
    "https://agroturismo.capixaba.dev",
]


def get_app() -> FastAPI:
    fast_app = FastAPI(
        title=APP_NAME,
        version=APP_VERSION,
        description=APP_DESCRIPTION,
        debug=IS_DEBUG,
    )
    fast_app.include_router(main_router, prefix=API_PREFIX)

    fast_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return fast_app


app = get_app()


@app.on_event("startup")
def on_startup():
    create_db_and_tables(engine)
