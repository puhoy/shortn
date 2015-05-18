__author__ = 'meatpuppet'


import unittest
import app
from app import create_app, db
from flask import current_app, url_for

from app.shortn.shortn import _standardize_url, \
    _convert_to_code, \
    _resolve_to_id, \
    ALPHABET, \
    _is_valid_short, \
    lengthen_url, shorten_url

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
        self.assertTrue(_is_valid_short(short+'a'))
        self.assertTrue(_is_valid_short(short+'aaa'))
        self.assertTrue(_is_valid_short(short+'#') == False)
        self.assertFalse(_is_valid_short('http://sadasda.de/a'))

    def test__standardize_url(self):
        urls = {'https://abc.de': 'https://abc.de/',
                'abc.de': 'http://abc.de/',
                'abc.de/ABc': 'http://abc.de/ABc',
                'ftp://abc.de/': 'ftp://abc.de/',
                'http://abc.de/<br>': 'http://abc.de/<br>',
                'http://abc.de/</br>': 'http://abc.de/</br>',
                'sftp://asdfasdf.de/AAA': 'sftp://asdfasdf.de/AAA',
                'abc:2323': 'http://abc:2323/'}
        no_urls = ['/google/',
                   '',
                   'abc/',
                   ]
        for given, standardized in urls.items():
            #print('')
            #print(given + "->" + _standardize_url(given))
            self.assertEqual(standardized, _standardize_url(given))
        for url in no_urls:
            self.assertEqual(_standardize_url(url), None)

    def test_shorten_url(self):
        db.session.remove()
        #should gibe the first char in alphanet
        code, long_url = shorten_url('hupen.de')
        self.assertEqual(code, ALPHABET[1], msg=code)
        self.assertTrue(code == ALPHABET[1])

        #should return the same if the link is already shortened
        code, long_url = shorten_url('hupen.de')
        self.assertTrue(code == ALPHABET[1])

        #next row
        code, long_url = shorten_url('hupen.de/a')
        self.assertTrue(code == ALPHABET[2])

        #no valid url
        code, long_url = shorten_url('hupen')
        self.assertEqual(code, None)

        #an valid shortened link should return its code again
        code, long_url = shorten_url(url_for('main.index', _external=True)+ALPHABET[1])
        self.assertEqual(code, ALPHABET[1])

    def test_lengthen_url(self):
        code, long_url = shorten_url('hupen.de')
        self.assertEqual(long_url, lengthen_url(code))
        self.assertEqual(False, lengthen_url('NOTYET'))
        self.assertEqual(False, lengthen_url('##'))  # not in alphabet



