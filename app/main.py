from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import auth_router  # Import the router module
from app.infrastructure.database.db import engine, Base

# Create tables (for development only)
# In production, use Alembic migrations
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Casa Serenity Backend",
    description="Real Estate Application API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware (Optional but recommended for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
# Ensure the prefix matches what you expect (e.g., /auth)
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Casa Serenity API"}