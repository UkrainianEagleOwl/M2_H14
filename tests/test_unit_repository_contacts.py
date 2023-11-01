

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

import datetime
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.database.models import Contact, User
from src.schemas import ContactCreate, ContactUpdate
from src.repository.contacts import (
    get_contact,
    get_contacts,
    create_contact,
    update_contact,
    delete_contact,
    search_contacts,
    get_contacts_with_birthdays
)

class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a mock session object and a user object.
        
        :param self: Represent the instance of the class
        :return: A user object with the id 1
        :doc-author: Trelent
        """
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        """
        The test_get_contacts function tests the get_contacts function.
        
        :param self: Represent the instance of the class
        :return: The contacts list
        :doc-author: Trelent
        """
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        """
        The test_get_contact_found function tests the get_contact function when a contact is found.
            It does this by mocking the session and returning a Contact object from it.
            The result of calling get_contact should be that same Contact object.
        
        :param self: Represent the instance of the class
        :return: The contact object
        :doc-author: Trelent
        """
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        """
        The test_get_contact_not_found function tests the get_contact function when a contact is not found.
            The test_get_contact_not_found function uses the mock library to create a mock session object, and then sets 
            that object's query method to return another mock object. This second mock has its filter method set to return 
            yet another mock, which in turn has its first method set to return None. This simulates what happens when no 
            contacts are found in the database for this user.
        
        :param self: Access the attributes and methods of the class in python
        :return: None
        :doc-author: Trelent
        """
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        """
        The test_create_contact function tests the create_contact function.
            It creates a ContactCreate object, and then uses that to create a Contact object.
            The session is mocked out so that it returns None when commit() is called on it, and 
            refreshes the contact after adding it to the session. Then we call our function with 
            these objects as arguments, and assert that its return value has both name and user_id equal to those of our contact.
        
        :param self: Refer to the current object
        :return: A contact object with the name and user_id attributes set to the values passed in
        :doc-author: Trelent
        """
        contact_data = ContactCreate(name="test name")
        contact = Contact(name=contact_data.name, user_id=self.user.id)
        self.session.add(contact)
        self.session.commit.return_value = None
        self.session.refresh(contact)
        result = await create_contact(contact=contact_data, user=self.user, db=self.session)
        self.assertEqual(result.name, contact_data.name)
        self.assertEqual(result.user_id, self.user.id)

    async def test_update_contact_found(self):
        """
        The test_update_contact_found function tests the update_contact function when a contact is found.
        It does this by creating a ContactUpdate object with an updated name, and then creates a Contact object with id 1 and user_id equal to self.user.id (which was created in setUp).
        Then it sets the return value of session's query().filter().first() method to be the contact we just created, so that when update_contact calls db.query(Contact).filter(Contact.id == contact_id), it will find our test Contact object instead of querying for one from the database (since we don't have any contacts
        
        :param self: Represent the instance of the class
        :return: A contact with the updated name
        :doc-author: Trelent
        """
        contact_data = ContactUpdate(name="updated name")
        contact = Contact(id=1, user_id=self.user.id)
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        self.session.refresh(contact)
        result = await update_contact(contact_id=1, contact=contact_data, user=self.user, db=self.session)
        self.assertEqual(result.name, contact_data.name)

    async def test_update_contact_not_found(self):
        """
        The test_update_contact_not_found function tests the update_contact function when a contact is not found.
            The test_update_contact_not_found function uses the following fixtures:
                - self.user, which is a User object with an id of 1 and an email address of 'test@example.com'
                - self.session, which is a mock SQLAlchemy session object that returns None for all queries
        
        :param self: Represent the instance of the class
        :return: None
        :doc-author: Trelent
        """
        contact_data = ContactUpdate(name="updated name")
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, contact=contact_data, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_delete_contact_found(self):
        """
        The test_delete_contact_found function tests the delete_contact function when a contact is found.
            The test_delete_contact_found function creates a Contact object and assigns it to the variable contact.
            The test_delete_contact_found function then sets self.session's query method to return an object with a filter method that returns an object with first method that returns the value of contact, which is assigned to result by calling delete-contact with user=self.user and db=self.session as arguments.
        
        :param self: Access the attributes and methods of the class in python
        :return: The contact object
        :doc-author: Trelent
        """
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await delete_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_delete_contact_not_found(self):
        """
        The test_delete_contact_not_found function tests the delete_contact function when a contact is not found.
            The test_delete_contact_not_found function uses the mock library to create a fake session object and user object.
            The test then calls the delete contact function with an id of 1, which will return None because it does not exist in our fake database.
        
        :param self: Represent the instance of the class
        :return: None
        :doc-author: Trelent
        """
        self.session.query().filter().first.return_value = None
        result = await delete_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_search_contacts(self):
        """
        The test_search_contacts function tests the search_contacts function.
            It does this by mocking out the database session and returning a list of contacts with matching names.
            The test then asserts that the result is equal to those contacts.
        
        :param self: Access the attributes and methods of the class in python
        :return: A list of contacts
        :doc-author: Trelent
        """
        name = "test name"
        contacts = [Contact(name=name, user_id=self.user.id), Contact(name=name, user_id=self.user.id)]
        self.session.query().filter().all.return_value = contacts
        result = await search_contacts(db=self.session, user=self.user, name=name)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_birthdays(self):
        """
        The test_get_contacts_with_birthdays function tests the get_contacts_with_birthdays function.
        It does this by creating a mock session and user, then mocking the query method of the session to return a list of contacts with birthdays in between start and end dates.
        The test asserts that when get_contacts_with_birthdays is called with these mocked objects, it returns those contacts.
        
        :param self: Access the attributes and methods of the class in python
        :return: The contacts list
        :doc-author: Trelent
        """
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)
        contacts = [Contact(birthday=start_date, user_id=self.user.id)]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_with_birthdays(start_date, end_date, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

if __name__ == '__main__':
    unittest.main()
