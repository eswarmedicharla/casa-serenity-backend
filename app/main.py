from fastapi import FastAPI
from app.api.routers import auth_router

app = FastAPI(title="Casa Serenity Backend", version="1.0")
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])