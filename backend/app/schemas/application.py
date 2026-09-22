from datetime import datetime

from pydantic import BaseModel

from app.models.application_status import ApplicationStatus

class ApplicationCreate(BaseModel):
    company: str
    status: ApplicationStatus
    job_title: str
    location: str
    job_url: str
    source: str
    job_description: str
    model_config = {
            "from_attributes": True
        }


class ApplicationUpdate(BaseModel):
    company: str 
    job_title: str 
    location: str
    job_description: str 
    job_url: str 
    source: str 
    status: str 


class ApplicationResponse(BaseModel):
    id:int
    company: str
    job_title:str
    location:  str| None = None
    job_url: str
    job_description: str | None = None
    source: str | None = None
    status: str
    date_applied: datetime | None = None
    updated_at: datetime | None = None


    model_config = {
        "from_attributes": True
    }

class ApplicationPatch(BaseModel):
    company: str | None = None
    job_title: str | None = None
    location: str | None = None
    job_url: str | None = None
    source: str | None = None
    job_description: str | None = None
    status: str | None = None