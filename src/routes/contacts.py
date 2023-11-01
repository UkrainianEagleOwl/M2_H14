from typing import List

from fastapi import APIRouter, HTTPException, Depends, status,Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactResponse, ContactCreate, ContactUpdate
from src.repository import contacts as repository_contacts
from src.services.auth import Auth  # Import your Auth service here
from src.database.models import User
from datetime import datetime, timedelta

router = APIRouter(prefix="/contacts", tags=["contacts"])


# Add the Auth service as a dependency
def get_current_user(auth: Auth = Depends(Auth.get_current_user)):
    return auth


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    contacts = await repository_contacts.get_contacts(skip, limit,current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id,current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body,current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int, body: ContactUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    contact = await repository_contacts.update_contact(contact_id, body,current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.delete_contact(contact_id,current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.get("/search/", response_model=List[ContactResponse])
async def search_contacts(
    name: str = Query(None, description="Search by name"),
    surname: str = Query(None, description="Search by surname"),
    email: str = Query(None, description="Search by email"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    contacts = await repository_contacts.search_contacts(db,current_user,name, surname, email)
    return contacts

@router.get("/birthdays/", response_model=List[ContactResponse])
async def get_contacts_with_birthdays(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    today = datetime.now()
    next_week = today + timedelta(days=7)
    contacts = await repository_contacts.get_contacts_with_birthdays(today, next_week, current_user,db)
    return contacts