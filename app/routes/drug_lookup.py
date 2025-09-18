import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.service.drug_lookup_service import DrugLookupService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/drug-lookup", tags=["Drug Lookup"])


@router.get("")
async def drug_lookup(
    drug_names: str = Query(..., description="List of drug names to lookup comma separated"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Lookup multiple drug names in the database
    """
    try:
        # Validate query
        if not drug_names or not drug_names.strip():
            raise HTTPException(status_code=400, detail="Drug names cannot be empty")
        
        # Split comma-separated string and clean up whitespace
        drug_names_list = [name.strip() for name in drug_names.split(',') if name.strip()]
        
        if not drug_names_list:
            raise HTTPException(status_code=400, detail="No valid drug names provided")
        
        drug_lookup_service = DrugLookupService(db)
        all_results = []
        
        # Loop through each drug name and perform lookup
        for drug_name in drug_names_list:
            try:
                result = await drug_lookup_service.lookup_drug(drug_name)
                all_results.extend(result)
            except Exception as e:
                logger.warning(f"Error looking up drug '{drug_name}': {e}")
                # Continue with other drugs even if one fails
                continue
        
        return all_results
    except Exception as e:
        logger.error(f"Error in drug_lookup: {e}")
        raise HTTPException(status_code=500, detail=str(e))