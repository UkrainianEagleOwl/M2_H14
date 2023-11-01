from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from src.database.models import Contact, User
from src.schemas import ContactCreate, ContactUpdate
from datetime import datetime


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return (
        db.query(Contact)
        .filter(Contact.user_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def get_contact(contact_id: int, user: User, db: Session) -> Optional[Contact]:
    return (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )


async def create_contact(contact: ContactCreate, user: User, db: Session) -> Contact:
    db_contact = Contact(name=contact.name, user_id=user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


async def update_contact(
    contact_id: int, contact: ContactUpdate, user: User, db: Session
) -> Optional[Contact]:
    db_contact = (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


async def delete_contact(contact_id: int, user: User, db: Session) -> Optional[Contact]:
    db_contact = (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


async def search_contacts(
    db: Session, user: User, name: str = None, surname: str = None, email: str = None
) -> List[Contact]:
    query = db.query(Contact)
    if name:
        query = query.filter(and_(Contact.name.ilike(f"%{name}%"), Contact.user_id == user.id))
    if surname:
        query = query.filter(and_(Contact.surname.ilike(f"%{surname}%", Contact.user_id == user.id)))
    if email:
        query = query.filter(and_(Contact.email.ilike(f"%{email}%", Contact.user_id == user.id)))
    contacts = await query.all()
    return contacts


async def get_contacts_with_birthdays(
    start_date: datetime, end_date: datetime, user: User, db: Session
) -> List[Contact]:
    contacts = (
        db.query(Contact)
        .filter(and_(Contact.birthday.between(start_date.date(), end_date.date()), Contact.user_id == user.id))
        .all()
    )
    return contacts
