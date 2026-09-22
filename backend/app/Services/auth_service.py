from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository

from app.utils.security import (hash_password,verify_password, create_access_token)

def register_user(db:Session, name: str, email: str, password: str):

    user_repo = UserRepository(db)

    # check if user exist or not
    existing_user = user_repo.get_user_by_email(email)

    if existing_user:
        raise ValueError("User with this email already exists.")

    # hash the password
    hashed_password = hash_password(password)

    # create the user
    created_user = user_repo.create_user(name, email, hashed_password)

    return created_user

def login_user(db:Session, email: str, password: str):

    user_repo = UserRepository(db)

    # find user
    user = user_repo.get_user_by_email(email)

    if not user:
        raise ValueError('Invalid email or password')

    # verify password
    password_valid = verify_password(password, user.hashed_password)

    if not password_valid:
        raise ValueError('Invalid email or password.')

    # create jwt
    access_token = create_access_token({
        'sub': str(user.id) 
    })

    return access_token