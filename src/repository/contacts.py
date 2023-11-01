from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from src.database.models import Contact, User
from src.schemas import ContactCreate, ContactUpdate
from datetime import datetime


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts for the user.
        
    
    :param skip: int: Skip a number of contacts in the database
    :param limit: int: Limit the number of contacts returned
    :param user: User: Filter the contacts by user_id
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    return (
        db.query(Contact)
        .filter(Contact.user_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def get_contact(contact_id: int, user: User, db: Session) -> Optional[Contact]:
    """
    The get_contact function returns a contact from the database.
    
    :param contact_id: int: Specify the id of the contact we want to get
    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    return (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )


async def create_contact(contact: ContactCreate, user: User, db: Session) -> Contact:
    """
    The create_contact function creates a new contact in the database.
        Args:
            contact (ContactCreate): The ContactCreate object to be created.
            user (User): The User object that is creating the ContactCreate object.
            db (Session): A Session instance for interacting with the database.
    
    :param contact: ContactCreate: Pass the contact data to the function
    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
    db_contact = Contact(name=contact.name, user_id=user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


async def update_contact(
    contact_id: int, contact: ContactUpdate, user: User, db: Session
) -> Optional[Contact]:
    """
    The update_contact function updates a contact in the database.
    
    :param contact_id: int: Identify the contact that is being updated
    :param contact: ContactUpdate: Pass in the updated contact information
    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: The updated contact
    :doc-author: Trelent
    """
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
    """
    The delete_contact function deletes a contact from the database.
        Args:
            contact_id (int): The id of the contact to delete.
            user (User): The user who is deleting the contact.
            db (Session): A database session object for interacting with the database.
        Returns:
            Optional[Contact]: If successful, returns a Contact object representing 
                what was deleted from the database; otherwise, returns None.
    
    :param contact_id: int: Find the contact to delete
    :param user: User: Get the user from the database
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
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
    """
    The search_contacts function searches for contacts in the database.
        Args:
            db (Session): The database session to use.
            user (User): The user who is searching for contacts.
            name (str, optional): A string containing a contact's name to search by. Defaults to None.
            surname (str, optional): A string containing a contact's surname to search by. Defaults to None.&lt;/code&gt;
    
    :param db: Session: Pass the database session to the function
    :param user: User: Get the user_id of the current user
    :param name: str: Search for contacts by name
    :param surname: str: Filter the contacts by surname
    :param email: str: Filter the contacts by email
    :return: A list of contacts
    :doc-author: Trelent
    """
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
    """
    The get_contacts_with_birthdays function returns a list of contacts with birthdays between the start_date and end_date.
        Args:
            start_date (datetime): The beginning date to search for contacts with birthdays.
            end_date (datetime): The ending date to search for contacts with birthdays.
            user (User): A User object containing the id of the user who owns these Contacts.
            db (Session): An SQLAlchemy Session object used to query database tables in this function.
    
    :param start_date: datetime: Set the start date for the query
    :param end_date: datetime: Specify the end date of the range
    :param user: User: Get the user's contacts
    :param db: Session: Connect to the database
    :return: A list of contacts with birthdays between the start and end dates
    :doc-author: Trelent
    """
    contacts = (
        db.query(Contact)
        .filter(and_(Contact.birthday.between(start_date.date(), end_date.date()), Contact.user_id == user.id))
        .all()
    )
    return contacts
