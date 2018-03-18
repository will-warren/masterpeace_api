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
        self.textmp = {'title': "Watermelons",
                 'author': "Charles Simic",
                 'post': "Green Buddhas / On the fruit stand / We eat the smiles / And spit out the teeth"}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_create(self):
        """Test API can create a TextMP (POST request)"""
        res = self.client().post('/textmp/', data=self.textmp)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Watermelons', str(res.data))

    def test_retrieve_all(self):
        """Test API can get a TextMP (GET request)."""
        res = self.client().post('/textmp/', data=self.textmp)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/textmp/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Watermelons', str(res.data))

    def test_retrieve_by_id(self):
        """Test API can get a single TextMP by using it's id."""
        rv = self.client().post('/textmp/', data=self.textmp)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/textmp/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Watermelons', str(result.data))

    def test_update(self):
        """Test API can edit an existing TextMP. (PUT request)"""
        rv = self.client().post(
            '/textmp/',
            data={'title': "Watermelons",
                 'author': "Charles Simic",
                 'post': "Green Buddhas / On the fruit stand / We eat the smiles / And spit out the teeth"
            })
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/textmp/1',
            data={'title': "Jazz",
                   'author': "Van G. Garrett",
                   'post': "we sing funk jazz groove \n we very seldom play blues \n our duet is cool"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/textmp/1')
        self.assertIn('Dont just eat', str(results.data))

    def test_delete(self):
        """Test API can delete an existing TextMP. (DELETE request)."""
        rv = self.client().post(
            '/textmp/',
            data={'title': "Watermelons",
                 'author': "Charles Simic",
                 'post': "Green Buddhas / On the fruit stand / We eat the smiles / And spit out the teeth"})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/textmp/1')
        self.assertEqual(res.status_code, 200)
        # 404 if post DNE
        result = self.client().get('/textmp/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()