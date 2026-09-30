from fastapi import Header, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.utils.security import SECRET_KEY, ALGORITHM
from app.models.users import User
from app.database.connection import get_db


def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    try:
        # split breaer token
        scheme, token = authorization.split(' ')

        #  check authorization scheme
        if scheme.lower() != 'bearer' :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )

        payload = jwt.decode(
            token, SECRET_KEY, algorithm=[ALGORITHM]
        )

        # get userId from sub
        user_id = payload.get('sub')

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token')

        # find user in database
        user = db.query(User).filter(User.id == int(user_id)).first
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return user

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )