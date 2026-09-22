from sqlalchemy.orm import Session

from app.models.application import Application

def create_application(db: Session, application: Application):
    db.add(application)
    db.commit()
    db.refresh(application)

    return application

def get_application(db: Session):
    return db.query(Application).all()

def get_application_by_id(db: Session, application_id: int):
    return db.query(Application).filter(Application.id == application_id).first()

def get_application_by_job_title(db: Session, job_title: str):
    return db.query(Application).filter(Application.job_title == job_title)

def update_application(db: Session, application_id: int, application: Application):
    db.commit()
    db.refresh(application)

    return application

def delete_application(db: Session, application: Application):
    db.delete(application)
    db.commit()