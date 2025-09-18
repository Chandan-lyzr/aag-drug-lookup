from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.ProviderDrugs import ProviderDrugs
import logging

logger = logging.getLogger(__name__)

class DrugLookupService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def lookup_drug(self, drug_name: str) -> Sequence[ProviderDrugs]:
        try:
            query = select(ProviderDrugs).where(ProviderDrugs.name.ilike(f"%{drug_name}%"))

            result = await self.db.execute(query)
            data = result.scalars().all()
            return data
        except Exception as e:
            logger.error(f"Error in lookup_drug: {e}")
            raise e