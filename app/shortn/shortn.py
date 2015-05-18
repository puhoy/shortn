__author__ = 'meatpuppet'

from ..models.Url import Url, db

import app

from flask import url_for, current_app
import re
from urllib import parse
import urltools

ALPHABET = "abcdefghijkmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# djangos url validator
url_regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
    r'localhost|' # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


#url_regex = re.compile('^(http(?:s)?\:\/\/[a-zA-Z0-9]+(?:(?:\.|\-)[a-zA-Z0-9]+)+(?:\:\d+)?(?:\/[\w\-]+)*(?:\/?|\/\w+\.[a-zA-Z]{2,4}(?:\?[\w]+\=[\w\-]+)?)?(?:\&[\w]+\=[\w\-]+)*)$')
##this should match valid urls, but protocol-agnostic
#url_regex = re.compile('^([a-z]+\:\/\/[a-zA-Z0-9]+(?:(?:\.|\-)[a-zA-Z0-9]+)+(?:\:\d+)?(?:\/[\w\-]+)*(?:\/?|\/\w+\.[a-zA-Z]{2,4}(?:\?[\w]+\=[\w\-]+)?)?(?:\&[\w]+\=[\w\-]+)*)$')

our_short_url_regex = None
# TODO set MAX_URLs somehow


def _convert_to_code(num, alphabet=ALPHABET):
    """
    stolen from  http://code.activestate.com/recipes/65212/
    """
    b = len(alphabet)
    return ((num == 0) and alphabet[0] ) or ( _convert_to_code(num // b, alphabet).lstrip(alphabet[0]) + alphabet[num % b])


def _resolve_to_id(code, alphabet=ALPHABET):
    '''https://github.com/jessex/shrtn/blob/master/shrtn.py'''
    """Converts the shortened URL code back to an id number in decimal form. Use
    the id to query the database and lookup the long URL."""
    base = len(alphabet)
    size = len(code)
    id = 0
    try:
        for i in range(0, size): #convert from higher base back to decimal
            id += alphabet.index(code[i]) * (base ** (size-i-1))
    except(ValueError):
        return False
    return id


def _is_valid_short(url):
    """
    this checks if a given url is one of our shortened urls
    on the first call this will create a regex which will be used in later calls.

    :param url:
    :return: True, if url is one of our valid short urls
    """
    global our_short_url_regex
    if not our_short_url_regex:
        our_short_url_regex = re.compile(url_for('main.index', _external=True) + "[a-zA-Z0-9]+$") #matches our URLs
    return not (not our_short_url_regex.match(url))


def _standardize_url(url):
    """Takes in a url and returns a clean, consistent format. For example:
    example.com, http://example.com, example.com/ all are http://example.com/
    Returns None if the url is somehow invalid."""
    parts = parse.urlparse(url, "http") #default scheme is http if omitted
    standard = parts.geturl()
    standard = urltools.normalize(standard)
    if not url_regex.match(standard):
        return None
    return standard


def shorten_url(url):
    """
    takes a url as argument and returns the short code (based on the db-row) and the normalized(!) long url
    if the url is already in the db, the old code is returned. if not, a new entry will be added (with timestamp,
    zero clicks and so on... see models/Url.py for more information)

    returns none if the url was invalid.

    :param url: a long url
    :return: shortened code, normalized url
    """
    if _is_valid_short(url):  # dont short our short urls
        code = url[len(url_for('main.index', _external=True)):]
        long_url = lengthen_url(code)
        if long_url:
            return code, long_url
        else:
            return None, None
    url = _standardize_url(url)
    if not url:
        return None, None

    #get the id for this url (whether new or otherwise)
    link = Url.query.filter_by(url=url).first()
    if not link: #url not yet inserted into database
        link = Url(url=url)
        db.session.add(link) #insert and get its id
        db.session.commit()
    code = _convert_to_code(link.id)
    return code, url


def lengthen_url(code):
    """
    Takes in one of our short-codes and returns the correct long url.

    :param code:
    :return:
    """
    id = _resolve_to_id(code) #convert shortened code to id
    if id:
        long = Url.query.filter_by(id=id).first()
        if not long: #id was not found in database
            return False
        long.clicks += 1
        db.session.add(long)
        return long.url #url to perform 301 re-direct on
    return False
