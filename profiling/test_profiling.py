__author__ = 'meatpuppet'

import unittest
from app import create_app, db

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

from app.shortn.shortn import shorten_url, lengthen_url, _convert_to_code
from flask import url_for

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

    def test_profile(self):
        profile_lengthen()
        profile_shorten()


def profile_shorten(output_file='profile_shorten.png'):
    with PyCallGraph(output=GraphvizOutput(output_file=output_file)):
        cnt = 50
        for i in range(0, cnt):
            shorten_url('http://abc.de/'+str(i))


def profile_lengthen(output_file='profile_lengthen.png'):
    with PyCallGraph(output=GraphvizOutput(output_file=output_file)):
        cnt = 10000
        url = url_for('main.index')
        for i in range(0, cnt):
            lengthen_url(url+str(_convert_to_code(i)))


def profile_api_shorten(output_file='profile_shorten.png'):
    with PyCallGraph(output=GraphvizOutput(output_file=output_file)):
        cnt = 50
        for i in range(0, cnt):
            shorten_url('http://abc.de/'+str(i))


def profile_api_lengthen(output_file='profile_lengthen.png'):
    with PyCallGraph(output=GraphvizOutput(output_file=output_file)):
        cnt = 10000
        url = url_for('main.index')
        for i in range(0, cnt):
            lengthen_url(url+str(_convert_to_code(i)))