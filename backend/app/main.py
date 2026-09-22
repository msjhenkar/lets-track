from fastapi import FastAPI
from app.database.connection import engine, Base
from app.routers import application_router, auth_router
from app.models.application import Application

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(application_router.router)
app.include_router(auth_router.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Job Application API!"}