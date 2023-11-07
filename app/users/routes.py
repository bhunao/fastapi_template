from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from app.database import get_session

from . import domain, schemas
from .domain import CurrentUserAnnotated


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/me", response_model=schemas.User)
def read_current_user(
        current_user: CurrentUserAnnotated
):
    assert current_user
    return current_user


@router.get("/all", response_model=list[schemas.User])
def read_all_users(
        current_user: CurrentUserAnnotated,
        skip: int = 0, limit: int = 100,
        session: Session = Depends(get_session),
):
    assert current_user
    users = domain.get_users(session=session, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    current_user: CurrentUserAnnotated,
    session: Session = Depends(get_session),
):
    assert current_user
    db_user = domain.get_user(session=session, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
