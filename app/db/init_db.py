from app.db.session import engine, Base

# function to initialize the asyncdatabase
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
