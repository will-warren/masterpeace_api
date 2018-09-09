import unittest
import os
import json
from app import create_app, db

class TextMPTestCase(unittest.TestCase):
    """This class represents the TextMP test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.textmp = {"title": "Watermelons",
                 "author": 1,
                 "post": "Green Buddhas / On the fruit stand / We eat the smiles / And spit out the teeth"}

        with self.app.app_context():
            db.create_all()

    def register_user(self, email="test@will.com", password="tarheels", quip="gogogo", location="durham",
                        photo="http://test-photo.com/me", user_name="algernon"):
        """Registers a test user"""
        user_data = {
            'email': email,
            'password': password,
            'location': location,
            'quip': quip,
            'photo': photo,
            'user_name': user_name
        }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email="test@will.com", password="tarheels"):
        """Logs in a test user"""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)

    def test_create(self):
        """Test API can create a TextMP (POST request)"""

        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/textmp/', headers=dict(Authorization="Bearer " +access_token), data=self.textmp)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Watermelons', str(res.data))

    def test_retrieve_all(self):
        """Test API can get a TextMP (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/textmp/', headers=dict(Authorization="Bearer " +access_token), data=self.textmp)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/textmp/', headers=dict(Authorization="Bearer " +access_token), data={'author': self.textmp['author']})
        self.assertEqual(res.status_code, 200)
        self.assertIn('Watermelons', str(res.data))

    def test_retrieve_by_id(self):
        """Test API can get a single TextMP by using it's id."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post('/textmp/', headers=dict(Authorization="Bearer " +access_token), data=self.textmp)
        self.assertEqual(rv.status_code, 201)

        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/textmp/{}'.format(int(result_in_json['data'][0]['id'])), 
            headers=dict(Authorization="Bearer " +access_token)
            )

        self.assertEqual(result.status_code, 200)
        self.assertIn('Watermelons', str(result.data))

    def test_update(self):
        """Test API can edit an existing TextMP. (PUT request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/textmp/',
            headers=dict(Authorization="Bearer " +access_token),
            data={"title": "Watermelons",
                 "author": 1,
                 "post": "Green Buddhas / On the fruit stand / We eat the smiles / And spit out the teeth"
            })
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/textmp/1',
            headers=dict(Authorization="Bearer " +access_token),
            data={"title": "Jazz",
                  "author": 1,
                  "post": "we sing funk jazz groove \n we very seldom play blues \n our duet is cool"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/textmp/1', headers=dict(Authorization="Bearer " +access_token))
        self.assertIn('we sing funk jazz groove', str(results.data))

    def test_delete(self):
        """Test API can delete an existing TextMP. (DELETE request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/textmp/',
            headers=dict(Authorization="Bearer " +access_token),
            data={"title": "Watermelons",
                 "author": 1,
                 "post": "Green Buddhas / On the fruit stand / We eat the smiles / And spit out the teeth"
            })
        self.assertEqual(rv.status_code, 201)

        res = self.client().delete('/textmp/1', headers=dict(Authorization="Bearer " +access_token))
        self.assertEqual(res.status_code, 200)

        # 404 if post DNE
        result = self.client().get('/textmp/1', headers=dict(Authorization="Bearer " +access_token))
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()