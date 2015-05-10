__author__ = 'meatpuppet'


import unittest
from app import create_app, db
from flask import current_app, url_for
from app.api.commands import status, \
    shorten, \
    expand, \
    most_clicked, \
    latest
import json

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client(use_cookies=True)

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_status(self):
        s = json.loads(status().get_data(as_text=True))
        self.assertEqual(s.get('status'), 'running')

    def test_shorten_put(self):
        #we put a url to short, and get an ok..
        response = self.client.put(url_for('api.shorten') + '?url=abc.de')
        s = json.loads(response.get_data(as_text=True))
        self.assertEqual(s.get('status'), 'ok')

        #were putting an invalid url
        response = self.client.put(url_for('api.shorten') + '?url=abc')
        s = json.loads(response.get_data(as_text=True))
        self.assertEqual(s.get('status'), 'err')

        #were putting an empty string
        response = self.client.put(url_for('api.shorten') + '?url=')
        s = json.loads(response.get_data(as_text=True))
        self.assertEqual(s.get('status'), 'err')

        #were putting an empty string
        response = self.client.put(url_for('api.shorten') + '')
        s = json.loads(response.get_data(as_text=True))
        self.assertEqual(s.get('status'), 'err')


    def test_expand(self):
        # non-existing code
        code = 'ZZZ'
        response = self.client.get(url_for('api.expand', code=code))
        s = json.loads(response.get_data(as_text=True))
        self.assertEqual(s.get('status'), 'err')
        self.assertEqual(s.get('url', None), None)

        #code not in alphabet
        code = '#+'
        response = self.client.get(url_for('api.expand', code=code))
        s = json.loads(response.get_data(as_text=True))
        self.assertEqual(s.get('status'), 'err')
        self.assertEqual(s.get('url', None), None)

        #no code
        code = ''
        url = url_for('api.expand', code=code)
        response = self.client.get(url)
        s = json.loads(response.get_data(as_text=True))
        self.assertEqual(s.get('status', None), 'err')
        self.assertEqual(s.get('url', None), None)

        #perfectly fine call (generate a new code, then expand it)
        response = self.client.put(url_for('api.shorten') + '?url=abc.de')
        s = json.loads(response.get_data(as_text=True))
        code1 = s.get('code')
        response = self.client.get(url_for('api.expand', code=code1))
        s = json.loads(response.get_data(as_text=True))
        self.assertEqual(s.get('status'), 'ok')
        self.assertEqual(s.get('url'), 'http://abc.de/')

        #perfectly fine call (generate a new code, then expand it)
        response = self.client.put(url_for('api.shorten') + '?url=abcd.de')
        s = json.loads(response.get_data(as_text=True))
        code2 = s.get('code')
        response = self.client.get(url_for('api.expand', code=code2))
        s = json.loads(response.get_data(as_text=True))
        self.assertEqual(s.get('status'), 'ok')
        self.assertEqual(s.get('url'), 'http://abcd.de/')

        # the last codes should be different
        self.assertFalse(code1 == code2)

    def test_most_clicked(self):
        pass

    def test_latest(self):
        pass