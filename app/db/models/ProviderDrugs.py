from sqlalchemy import Column, Integer, String
from app.db.database import Base


class ProviderDrugs(Base):
    __tablename__ = "provider_drugs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(1000))
    tier = Column(String(500))
    restrictions = Column(String(1000))
    provider = Column(String(50))