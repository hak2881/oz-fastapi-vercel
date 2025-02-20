from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import hash_password, verify_password, create_token, get_current_user
from database import get_db
from models import User
from schemas import UserCreateSchema, UserLoginSchema

user_router = APIRouter(
    tags=["User"]
)

@user_router.post("/register")
async def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    new_user = User(
        username = user.username,
        password = hash_password(user.password),
        email = user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": f"Success Created user {new_user.username}"}

@user_router.post("/login")
async def login(user: UserLoginSchema, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username==user.username).first()

    if not existing_user :
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(
            status_code=404,
            detail="Password not verify"
        )
    access_token = create_token(data={"sub": existing_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.get("/profile")
async def user_detail(user: dict = Depends(get_current_user)):
    return user

