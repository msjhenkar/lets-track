
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.sql import func

from sqlalchemy import Enum

from app.models.application_status import ApplicationStatus

from sqlalchemy import Column

from app.database.connection import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, autoincrement=True)

    company = Column(String(100), nullable=False)
    job_title = Column(String(225), nullable=False)
    location = Column(String(100), nullable=False)

    job_url = Column(String(500), nullable=False)
    source = Column(String(100), nullable=True)

    status = Column(Enum(ApplicationStatus), nullable=False)

    job_description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    date_applied = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
