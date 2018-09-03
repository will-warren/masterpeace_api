import unittest
import os
import json
from app import create_app, db

class UserTestCase(unittest.TestCase):
    """This class represents the TextMP test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {
            "email": "test_script@test.com",
            "password": "abcd1234%",
            "location": "Durham",
            "quip": "witty test remark",
            "photo": "http://photoimage.com",
            "user_name": "test_name"
        }

        with self.app.app_context():
            db.create_all()

    def register_user(self):
        """Registers a test user"""
        user_data = {
            'email': self.user['email'],
            'password': self.user['password'],
            'location': self.user['location'],
            'quip': self.user['quip'],
            'photo': self.user['photo'],
            'user_name': self.user['user_name']
        }
        return self.client().post('/auth/register',  data=user_data)

    def login_user(self):
        """Logs in a test user"""
        user_data = {
            'email': self.user['email'],
            'password': self.user['password']
        }
        return self.client().post('/auth/login', data=user_data)

    def test_get_user(self):
        """tests api returns a user model"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().get('/users/{}'.format(self.user['email']), headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('test_name', str(res.data))

    def test_delete_user(self):
        """tests api can delete a user"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().delete('/users/{}'.format(self.user['email']), headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        # 404 if user DNE
        result = self.client().get('/users/{}'.format(self.user['email']), headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def test_update_user(self):
        """tests api can update a user model"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().put('/users/{}'.format(self.user['email']), headers=dict(Authorization="Bearer " + access_token), 
            data={'location': 'Raleigh', 'user_name': 'new name', 'quip': 'boo dap doo bah', 'photo': 'ellis.png'})
        self.assertEqual(result.status_code, 200)
        self.assertIn('Raleigh', str(res.data))
        self.assertIn('new name', str(res.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()