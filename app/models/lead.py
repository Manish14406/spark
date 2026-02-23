from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
from sqlalchemy import UniqueConstraint


class Lead(Base):
    __tablename__ = "leads"

    __table_args__ = (
    UniqueConstraint('creator_id', 'email', name='unique_creator_email'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("creators.id"))
    name = Column(String)
    email = Column(String, nullable=False)
    phone = Column(String)
    source = Column(String)
    status = Column(String, default="new")
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("Creator")