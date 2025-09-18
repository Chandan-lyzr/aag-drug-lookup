import uvicorn
import logging
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from app.core.logging import setup_logging
from app.db.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.routes.drug_lookup import router as drug_lookup

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    # lifespan=lifespan,
    title=settings.project_name,
    docs_url="/docs",
    version=settings.version,
)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
 
@app.on_event("startup")
def on_startup():
    logger.info("Server is starting...")
 
@app.get("/", tags=["root"])
async def read_root(db: AsyncSession = Depends(get_db_session)):
    return f"{settings.environment} Server is Up"
 
 
# Routers
app.include_router(drug_lookup)
 
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)