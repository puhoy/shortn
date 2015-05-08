__author__ = 'meatpuppet'


import unittest
from app import create_app, db
from flask import current_app, url_for

from app.shortn.shortn import _standardize_url, _convert_to_code, _resolve_to_id, ALPHABET, _is_valid_short

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test__resolve_to_id(self):
        id = 6
        code = ALPHABET[6]
        self.assertTrue(_resolve_to_id(code) == id)
        self.assertFalse(_resolve_to_id(code) == id+1)
        self.assertTrue(_resolve_to_id('', alphabet='a') == 0)
        self.assertTrue(_resolve_to_id('a', alphabet='ab') == 0)
        self.assertTrue(_resolve_to_id('b', alphabet='ab') == 1)
        self.assertTrue(_resolve_to_id('ba', alphabet='ab') == 2)
        #value errors: searching 'b' in alphabet 'a'
        self.assertFalse(_resolve_to_id('ab', alphabet='a') == 1)
        pass

    def test__convert_to_code(self):
        self.assertTrue(_convert_to_code(0, alphabet='ab') == 'a')
        self.assertTrue(_convert_to_code(1, alphabet='ab') == 'b')
        self.assertTrue(_convert_to_code(2, alphabet='ab') == 'ba')
        self.assertTrue(_convert_to_code(3, alphabet='ab') == 'bb')
        self.assertTrue(_convert_to_code(4, alphabet='ab') == 'baa')
        self.assertTrue(_convert_to_code(5, alphabet='ab') == 'bab')
        self.assertTrue(_convert_to_code(6, alphabet='ab') == 'bba')
        self.assertTrue(_convert_to_code(7, alphabet='ab') == 'bbb')
        self.assertTrue(_convert_to_code(0, alphabet='01') == '0')
        self.assertTrue(_convert_to_code(1, alphabet='01') == '1')
        self.assertTrue(_convert_to_code(2, alphabet='01') == '10')

    def test__is_valid_short(self):
        short = url_for('main.index', _external=True)
        self.assertTrue(_is_valid_short(short+'a') == True)
        self.assertTrue(_is_valid_short(short+'aaa') == True)
        self.assertTrue(_is_valid_short(short+'#') == False)

    def test__standardize_url(self):
        urls = {'google': 'http://google/',
                'https://abc.de': 'https://abc.de/',
                '': 'http:///'}
        for given, standardized in urls.items():
            #print('')
            #print(given + "->" + _standardize_url(given))
            self.assertTrue(standardized == _standardize_url(given))

