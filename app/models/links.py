__author__ = 'meatpuppet'



from app import db


class Link(db.Model):
    """

    """
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048))

