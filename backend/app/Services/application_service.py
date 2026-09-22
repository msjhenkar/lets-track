from sqlalchemy.orm import Session

from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationPatch

from app.repositories import application_repository


def create_application(db: Session, application_data: ApplicationCreate):

    application = Application(
        company = application_data.company,
        job_title = application_data.job_title,
        status = application_data.status,
        job_description = application_data.job_description,
        job_url = application_data.job_url,
        location = application_data.location,
        source = application_data.source,
    )

    return application_repository.create_application(db, application)

def get_application(db: Session):
    return application_repository.get_application(db)

def get_application_by_id(db: Session, application_id: int):
    return application_repository.get_application_by_id(db, application_id)

def get_application_by_job_title(db: Session, job_title: str):
    return application_repository.get_application_by_job_title(db, job_title)

def update_application(db: Session, application_id: int, application_data: ApplicationUpdate):
    application = application_repository.get_application_by_id(db, application_id)

    if application is None:
        return None

    application.company = application_data.company
    application.job_title = application_data.job_title
    application.location = application_data.location
    application.job_description = application_data.job_description
    application.job_url = application_data.job_url
    application.source = application_data.source
    application.status = application_data.status

    return application_repository.update_application(db, application_id, application)

def delete_application(db: Session, application_id: int):
    application = application_repository.get_application_by_id(db, application_id)

    if application is None:
        return None

    application_repository.delete_application(db, application)
    return application

def patch_application(db: Session, application_id: int, application_data: ApplicationPatch):
    application = application_repository.get_application_by_id(db, application_id)

    if application is None:
        return None

    if application_data.company is not None:
        application.company = application_data.company

    if application_data.job_title is not None:
        application.job_title = application_data.job_title

    if application_data.location is not None:
        application.location = application_data.location

    if application_data.job_description is not None:
        application.job_description = application_data.job_description

    if application_data.job_url is not None:
        application.job_url = application_data.job_url

    if application_data.source is not None:
        application.source = application_data.source

    if application_data.status is not None:
        application.status = application_data.status

    return application_repository.update_application(db, application_id, application)