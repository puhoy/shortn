__author__ = 'meatpuppet'

"""
THE WHOLE SHORTENING CODE
(which means the functions _convert_to_code, _resolve_to_id, _is_valid_short)
IS BASED ON https://github.com/jessex/shrtn/blob/master/shrtn.py !!!
"""

from ..models.Url import *

from flask import url_for
import re
from urllib import parse


import urltools

ALPHABET = "abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789"
#re_end = re.compile("[.][^/]+$") #for checking the end of a url
MAX_URLS = 10000


def _convert_to_code(id, alphabet=ALPHABET):
    """Converts a decimal id number into a shortened URL code. Use the id of the
    row in the database with the entered long URL."""
    if id <= 0: #invalid codes (autoincrement is always 1 or higher)
        return alphabet[0]
    base = len(alphabet) #base to convert to (56 for our standard alphabet)
    chars = []
    while id:
        chars.append(alphabet[id % base])
        id //= base
    chars.reverse() #moved right to left, so reverse order
    return ''.join(chars) #convert stored characters to single string


def _resolve_to_id(code, alphabet=ALPHABET):
    """Converts the shortened URL code back to an id number in decimal form. Use
    the id to query the database and lookup the long URL."""
    base = len(alphabet)
    size = len(code)
    id = 0
    for i in range(0, size): #convert from higher base back to decimal
        id += alphabet.index(code[i]) * (base ** (size-i-1))
    return id % MAX_URLS


def _is_valid_short(url):
    """Takes in a url and determines if it is a valid shortened url."""
    re_short = re.compile(url_for('main.index', _external=True) + "[a-kmnp-zA-HJ-NP-Z2-9]+$") #matches our URLs
    return not (not re_short.match(url))


def _standardize_url(url):
    """Takes in a url and returns a clean, consistent format. For example:
    example.com, http://example.com, example.com/ all are http://example.com/
    Returns None if the url is somehow invalid."""
    parts = parse.urlparse(url, "http") #default scheme is http if omitted
    if parts[0] != "http" and parts[0] != "https": #scheme was not http(s)
        return None
    standard = parts.geturl()
    standard = urltools.normalize(standard)
    return standard


def shorten_url(url):  # TODO search all uses!!
    """
    takes a url as argument and returns the short code (based on the db-row) and the normalized(!) long url
    if the url is already in the db, the old code is returned. if not, a new entry will be added (with timestamp,
    zero clicks and so on... see models/Url.py for more information)

    returns none if the url was invalid.

    :param url: a long url
    :return: shortened code, normalized url
    """
    if _is_valid_short(url):  # dont short our short urls
        return url[len(url_for('main.index', _external=True)):]
    url = _standardize_url(url)
    if url is None: #tried to shorten invalid url
        return None

    #get the id for this url (whether new or otherwise)
    link = Url.query.filter_by(url=url).first()
    if not link: #url not yet inserted into database
        link = Url(url=url)
        db.session.add(link) #insert and get its id
        db.session.commit()
    id = Url.query.filter_by(url=url).first().id
    code = _convert_to_code(id)
    return code, url


def lengthen_url(code):
    """Takes in one of our shortened URLs and returns the correct long url."""
    id = _resolve_to_id(code) #convert shortened code to id
    long = Url.query.filter_by(id=id).first()
    if not long: #id was not found in database
        return None
    long.clicks += 1
    db.session.add(long)
    return long.url #url to perform 301 re-direct on