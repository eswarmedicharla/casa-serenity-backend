from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import auth_router  # Import the router module
from app.infrastructure.database.db import engine, Base
from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException
from app.utils.response import error_response

app = FastAPI(
    title="Casa Serenity Backend",
    description="Real Estate Application API",
    version="1.0.0"
)

# CORS Middleware (Optional but recommended for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=exc.detail,
            code=exc.status_code
        )
    )
# Include Routers
# Ensure the prefix matches what you expect (e.g., /auth)
app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Casa Serenity API"}