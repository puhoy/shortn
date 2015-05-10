__author__ = 'meatpuppet'

import unittest
from app import create_app, db


from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

from app.shortn.shortn import shorten_url, lengthen_url, _convert_to_code
from flask import url_for
from app.models.Url import Url

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

    def test_profile_shorten(self, output_file='profile_shorten.png'):
        with PyCallGraph(output=GraphvizOutput(output_file=output_file)):
            cnt = 50
            for i in range(0, cnt):
                shorten_url('http://abc.de/'+str(i))

    def test_profile_lengthen(self, output_file='profile_lengthen.png'):
        with PyCallGraph(output=GraphvizOutput(output_file=output_file)):
            cnt = 100
            url = url_for('main.index')
            for i in range(0, cnt):
                lengthen_url(url+str(_convert_to_code(i)))

    def test_profile_api_shorten(self, output_file='profile_api_shorten.png'):
        with PyCallGraph(output=GraphvizOutput(output_file=output_file)):
            cnt = 50
            for i in range(0, cnt):
                self.client.put(url_for('api.shorten') + '?url=abc/' + str(i))

    def test_profile_api_lengthen(self, output_file='profile_api_lengthen.png'):
        cnt = 100
        #fill db with junk to test
        for x in range(0, cnt):
            url = 'http://abc.de/'+str(cnt)
            u = Url(url=url)
            db.session.add(u)
            db.session.commit()

        with PyCallGraph(output=GraphvizOutput(output_file=output_file)):
            for i in range(0, cnt):
                self.client.get(url_for('api.expand', code=cnt))
