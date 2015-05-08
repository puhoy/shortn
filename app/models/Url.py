__author__ = 'meatpuppet'

from app import db
import datetime



class Url(db.Model):
    """
    holds all url-related information

    for now it is only used by shortn/shortn.py
    """
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048))

    clicks = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)
    time_last_clicked = db.Column(db.DateTime)

    def __init__(self, url):
        self.url = url
        self.creation_date = datetime.datetime.now()
        self.time_last_clicked = datetime.datetime.now()
        self.clicks = 0

def upgrade_url():
    '''
    this function is probably never needed.
    it was written to set the new time and "clicks" field for older entries.

    :return:
    '''
    for url in Url.query.all():
        if url.creation_date is None:
            url.creation_date = datetime.datetime.now()
        if url.time_last_clicked is None:
            url.time_last_clicked = datetime.datetime.now()
        if url.clicks is None:
            url.clicks = 0