from sqlalchemy.orm import Session

from app.models.users import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email:str):
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, name: str, email: str, hashed_password:str):
        user = User(name=name, email=email, hashed_password=hashed_password)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user