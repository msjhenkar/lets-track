from fastapi import APIRouter, Depends, status, HTTPException, Header
from sqlalchemy.orm import Session

from app.Services.auth_service import (register_user, login_user)
from app.database.connection import get_db
from app.schemas.user import UserCreate, LoginRequest, LoginResponse, UserResponse
from app.utils.dependencies import get_current_user

router = APIRouter(
    prefix = "/auth",
    tags = ["authentication"]
)

@router.get("/test-auth")
def test_auth(current_user = Depends(get_current_user)):
    return {
        "message": "Authentication successful",
        "user_id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }


@router.post("/register",response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        registered_user = register_user(db = db,name= user.name, email=user.email, password=user.password)
        return registered_user

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post('/login', response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(user:LoginRequest, db: Session = Depends(get_db)):
    try: 
        access_token = login_user(
            db = db,
            email=user.email,
            password=user.password
        )

        return {
            'access_token': access_token,
            "token_type": "bearer"
        }
    
    except ValueError as e:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))