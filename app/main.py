from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from app.routers import news, homepage  # routers imports 
from app.db.init_db import init_db
from fastapi.staticfiles import StaticFiles
from app.agents.agent_context_class import AgentContext
from contextlib import asynccontextmanager
from app.services.logger import api_logger as logger

from pathlib import Path
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend" / "dist"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function creates the context for the lifespan of the application. It initializes the database.
    """
    try:
        await init_db()
        yield
    finally:
        pass

# initialize the FastAPI app with metadata
app = FastAPI(lifespan=lifespan)


# CORS Configuration 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domains in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

## API endpoints
app.include_router(homepage.router)
#app.include_router(news.router)


# Creating static file within our directory
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")