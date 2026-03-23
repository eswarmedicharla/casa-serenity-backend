from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib

# Connection parameters
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=EMPINHYL-082\\SQLEXPRESS01;"
    "DATABASE=RealEstateCasaSernityDb;"
    "Trusted_Connection=yes;"
)

DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# ✅ Sync Engine
engine = create_engine(DATABASE_URL, echo=True, future=True)

# ✅ Sync Session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# ✅ Sync DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()