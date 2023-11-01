from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
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
    """
    The get_current_user function is a dependency that will be injected into the
        function below. It will return the current user object, or None if no user
        is logged in.

    :param auth: Auth: Get the current user
    :return: An auth object
    :doc-author: Trelent
    """
    return auth


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    The get_contacts function returns a list of contacts for the current user.
        The function takes in three parameters: skip, limit and db.
        Skip is used to determine how many contacts to skip before returning results.
        Limit is used to determine how many contacts should be returned after skipping the specified number of records (skip).


    :param current_user: User: Get the current user from the database
    :param skip: int: Skip the first n contacts
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Access the database
    :param : Get the current user from the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    The get_contact function returns a contact by its id.

    :param contact_id: int: Specify the contact id that is passed in the url
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the repository layer
    :return: A contact with the given id, if it exists
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(
    body: ContactCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    The create_contact function creates a new contact in the database.


    :param body: ContactCreate: Pass the data from the request body to create_contact function
    :param current_user: User: Get the current user
    :param db: Session: Pass the database session to the repository layer
    :return: A contact object, which is the same as the body of a request
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    body: ContactUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactUpdate): The updated information for the specified Contact.
            current_user (User = Depends(get_current_user)): The user making this request, as determined by get_current_user().
            db (Session = Depends(get_db)): A database session object, as determined by get() from fastapi/database/crud.py.

    :param contact_id: int: Specify the contact to update
    :param body: ContactUpdate: Get the data from the request body
    :param current_user: User: Get the current user
    :param db: Session: Pass the database session to the repository layer
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(
        contact_id, body, current_user, db
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(
    contact_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    The delete_contact function deletes a contact from the database.
        Args:
            contact_id (int): The id of the contact to delete.
            current_user (User): The user who is making this request.
            db (Session, optional): SQLAlchemy Session instance. Defaults to Depends(get_db).

    :param contact_id: int: Get the contact id from the request url
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the repository layer
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.delete_contact(contact_id, current_user, db)
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
    """
    The search_contacts function searches for contacts in the database.
        It takes three optional parameters: name, surname and email.
        If no parameter is given, it returns all contacts of the current user.

    :param name: str: Search by name, the surname: str parameter is used to search by surname and the email: str parameter is used to search by email
    :param description: Document the endpoint in the openapi schema
    :param surname: str: Search by surname
    :param description: Document the api
    :param email: str: Search contacts by email
    :param description: Document the endpoint
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the repository layer
    :param : Search for a contact by name, surname or email
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.search_contacts(
        db, current_user, name, surname, email
    )
    return contacts


@router.get("/birthdays/", response_model=List[ContactResponse])
async def get_contacts_with_birthdays(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    The get_contacts_with_birthdays function returns a list of contacts with birthdays in the next week.


    :param current_user: User: Get the current user
    :param db: Session: Get the database session
    :return: A list of contacts with birthdays in the next 7 days
    :doc-author: Trelent
    """
    today = datetime.now()
    next_week = today + timedelta(days=7)
    contacts = await repository_contacts.get_contacts_with_birthdays(
        today, next_week, current_user, db
    )
    return contacts
