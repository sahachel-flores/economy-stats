from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from app.routers import news, homepage  # routers imports 
from app.db.init_db import init_db

# initialize the FastAPI app with metadata
app = FastAPI(
    title="Economy Stats AI",
    description="A FastAPI backend that uses AI agents to analyze and summarize the US economy.",
    version="1.0.0"
)

# Initialize the database
init_db()

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
app.include_router(news.router)


@app.get("/")
async def root():
    return {"message": "Hello to Economy Stats AI"}