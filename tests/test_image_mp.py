import unittest
import os
import json
from app import create_app, db

class ImageMPTestCase(unittest.TestCase):
    """This tests the ImageMP API routes"""

    def setUp(self):
        """Set ups vars for testing"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.imagemp = {"title": "Sun",
                 "author": 1,
                 "post": "https://en.wikipedia.org/wiki/Sun#/media/File:Sun_poster.svg"
        }

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
        return self.client().post('/auth/register',  data=user_data)

    def login_user(self, email="test@will.com", password="tarheels"):
        """Logs in a test user"""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)
    
    def test_create(self):
        """Tests creation of an ImageMP (POST)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/imagemp/', headers=dict(Authorization="Bearer " + access_token), data=self.imagemp)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Sun', str(res.data))

    def test_retrieve_all(self):
        """Tests retrieving all ImageMPs (GET)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/imagemp/', headers=dict(Authorization="Bearer " + access_token), data=self.imagemp)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/imagemp/', headers=dict(Authorization="Bearer " + access_token), data={'author': self.imagemp['author']})
        self.assertEqual(res.status_code, 200)
        self.assertIn('Sun', str(res.data))

    def test_retrieve_by_id(self):
        """Tests retrieving an ImageMP by its id (GET)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post('/imagemp/', headers=dict(Authorization="Bearer " + access_token), data=self.imagemp)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/imagemp/{}'.format(result_in_json['id']), 
            headers=dict(Authorization="Bearer " + access_token)
        )
        self.assertEqual(result.status_code, 200)
        self.assertIn('Sun', str(result.data))

    def test_update(self):
        """Tests updating an ImageMP (PUT)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/imagemp/',
            headers=dict(Authorization="Bearer " + access_token),
            data={"title": "Sun",
                 "author": 1,
                 "post": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Sun_poster.svg"
            })
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/imagemp/1',
            headers=dict(Authorization="Bearer " + access_token),
            data={"title": "Trombone",
                  "author": 1,
                  "post": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Posaune.jpg"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/imagemp/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Trombone', str(results.data))

    def test_delete(self):
        """Tests deleting an ImageMP (DELETE)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        req = self.client().post(
            '/imagemp/',
            headers=dict(Authorization="Bearer " + access_token),
            data={"title": "Sun",
                 "author": 1,
                 "post": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Sun_poster.svg"
            })
        self.assertEqual(req.status_code, 201)
        res = self.client().delete('/imagemp/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        # 404 if post DNE
        result = self.client().get('/imagemp/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()