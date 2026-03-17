from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import urllib

# Connection parameters
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=EMPINHYL-082\\SQLEXPRESS01;"
    "DATABASE=RealEstateCasaSernityDb;"
    "Trusted_Connection=yes;"
)

#Note: You must install aioodbc (pip install aioodbc) for SQL Server async support. 
#If you strictly must stick to pyodbc without aioodbc, 
#true async DB calls aren't possible without running them in a thread pool, which defeats the purpose. The code below assumes mssql+aioodbc.
# Note: We use mssql+pyodbc for sync, but for async with SQL Server, 
# you typically need 'mssql+aioodbc' or 'mssql+asyncpg' (if postgres). 
# Since you specified pyodbc, note that true async support for SQL Server via pyodbc is limited.
# To make this work with 'async', we usually switch to 'aioodbc'. 
# Assuming you have 'aioodbc' installed or will install it: 
# pip install aioodbc

DATABASE_URL = f"mssql+aioodbc:///?odbc_connect={params}"

# Create Async Engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session