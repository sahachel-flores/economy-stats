from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from app.routers import news, homepage  # routers imports 
from app.db.init_db import init_db
from fastapi.staticfiles import StaticFiles
from app.agents.agent_context_class import AgentContext
from contextlib import asynccontextmanager
from app.services.logger import api_logger as logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function creates the context for the lifespan of the application. It initializes the database.
    """
    app.state.context = AgentContext()
    try:
        await init_db()
        yield
    finally:
        pass

# initialize the FastAPI app with metadata
app = FastAPI(lifespan=lifespan)

# Creating static file within our directory
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend") 

# CORS Configuration 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domains in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello to Economy Stats AI"}

## API endpoints
app.include_router(homepage.router)
#app.include_router(news.router)


