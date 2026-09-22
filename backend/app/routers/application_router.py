from app.Services import application_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.application import ApplicationCreate, ApplicationPatch, ApplicationUpdate, ApplicationResponse
from app.database.connection import get_db

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)

@router.post("", response_model=ApplicationResponse)
def create_application(application_data: ApplicationCreate, db: Session = Depends(get_db)):
    application = application_service.create_application(db, application_data)
    return application

@router.get("", response_model=list[ApplicationResponse])
def get_application(db: Session = Depends(get_db)):
    applications = application_service.get_application(db)
    return applications

@router.get('/{application_id}', response_model=ApplicationResponse)
def get_application_by_id(application_id: int, db: Session = Depends(get_db)):
    application = application_service.get_application_by_id(db, application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.get('/{job_title}', response_model=ApplicationResponse)
def get_application_by_job_title(job_title: str, db: Session = Depends(get_db)):
    application = application_service.get_application_by_job_title(db, job_title)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(application_id: int, application_data: ApplicationUpdate, db: Session = Depends(get_db)):
    application = application_service.update_application(db, application_id, application_data)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.delete("/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    application = application_service.delete_application(db, application_id)

    if application is None:
        raise HTTPException(status_code=404, detail = "Application not found")

    return {"message": "Application deleted successfully"}

@router.patch("/{application_id}", response_model=ApplicationResponse)
def patch_application(application_id: int, application_data: ApplicationPatch, db: Session = Depends(get_db)):
    application = application_service.patch_application(db, application_id, application_data)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return application