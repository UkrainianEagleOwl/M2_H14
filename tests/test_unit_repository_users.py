
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
from unittest.mock import MagicMock
from src.database.models import User
from src.schemas import UserModel
from libgravatar import Gravatar
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
)

class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a mock database and a mock Gravatar object, which are used by the tests.
        
        :param self: Represent the instance of the object that is being created
        :return: A magicmock object
        :doc-author: Trelent
        """
        self.db = MagicMock()
        self.gravatar = MagicMock(spec=Gravatar)

    async def test_get_user_by_email_found(self):
        """
        The test_get_user_by_email_found function tests the get_user_by_email function when a user is found.
        
        :param self: Access the attributes and methods of the class in python
        :return: A user with an email address of test@example
        :doc-author: Trelent
        """
        email = "test@example.com"
        user = User(email=email)
        self.db.query().filter().first.return_value = user
        result = await get_user_by_email(email, db=self.db)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        """
        The test_get_user_by_email_not_found function tests the get_user_by_email function when a user with the given email does not exist.
        
        :param self: Access the attributes and methods of the class in python
        :return: None
        :doc-author: Trelent
        """
        email = "nonexistent@example.com"
        self.db.query().filter().first.return_value = None
        result = await get_user_by_email(email, db=self.db)
        self.assertIsNone(result)

    async def test_create_user(self):
        """
        The test_create_user function tests the create_user function.
        It does this by creating a user object, and then passing it to the create_user function.
        The test then checks that the email and avatar url are correct.
        
        :param self: Refer to the instance of the class
        :return: The result of the create_user function
        :doc-author: Trelent
        """
        user_data = UserModel(email="test@example.com")
        avatar_url = "http://example.com/avatar.jpg"
        self.gravatar.get_image.return_value = avatar_url
        new_user = User(**user_data.dict(), avatar=avatar_url)
        self.db.add(new_user)
        self.db.commit.return_value = None
        self.db.refresh(new_user)
        result = await create_user(body=user_data, db=self.db)
        self.assertEqual(result.email, user_data.email)
        self.assertEqual(result.avatar, avatar_url)

    async def test_update_token(self):
        """
        The test_update_token function tests the update_token function.
            It creates a user object and sets its refresh token to &quot;new_token&quot;.
            Then it calls the update_token function with that user and token, passing in our mock db.
            Finally, it asserts that the user's refresh token is equal to &quot;new_token&quot;.
        
        :param self: Access the attributes and methods of the class
        :return: None
        :doc-author: Trelent
        """
        user = User(email="test@example.com")
        token = "new_token"
        user.refresh_token = token
        self.db.commit.return_value = None
        await update_token(user, token, db=self.db)
        self.assertEqual(user.refresh_token, token)

    async def test_confirmed_email(self):
        """
        The test_confirmed_email function tests the confirmed_email function.
        It does this by creating a mock user object, setting its email to &quot;test@example.com&quot; and its confirmed attribute to False.
        Then it sets the return value of db's query().filter() method to be that mock user object, and sets db's commit() method's return value to None (since we don't care about what it returns).
        Finally, it calls the confirmed_email function with our mocked database as an argument (db=self.db), which should set our mock user object's confirmed attribute from False to True.
        
        :param self: Access the attributes and methods of the class in python
        :return: True
        :doc-author: Trelent
        """
        email = "test@example.com"
        user = User(email=email)
        user.confirmed = False
        self.db.query().filter().first.return_value = user
        self.db.commit.return_value = None
        await confirmed_email(email, db=self.db)
        self.assertTrue(user.confirmed)

    async def test_update_avatar(self):
        """
        The test_update_avatar function tests the update_avatar function.
        It creates a mock user, sets the avatar url to a new value, and then calls update_avatar with that email address.
        The result should be that the user's avatar is set to this new value.
        
        :param self: Access the class attributes and methods
        :return: The avatar_url, which is the same as the result
        :doc-author: Trelent
        """
        email = "test@example.com"
        user = User(email=email)
        avatar_url = "http://example.com/new_avatar.jpg"
        self.db.query().filter().first.return_value = user
        self.db.commit.return_value = None
        result = await update_avatar(email, avatar_url, db=self.db)
        self.assertEqual(result.avatar, avatar_url)

if __name__ == '__main__':
    unittest.main()
