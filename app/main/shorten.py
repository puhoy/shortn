__author__ = 'meatpuppet'


from ..models.links import *

from flask import current_app, url_for, abort
import sys, re
from urllib import parse

ALPHABET = "abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
re_end = re.compile("[.][^/]+$") #for checking the end of a url


def convert_to_code(id, alphabet=ALPHABET):
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


def resolve_to_id(code, alphabet=ALPHABET):
    """Converts the shortened URL code back to an id number in decimal form. Use
    the id to query the database and lookup the long URL."""
    base = len(alphabet)
    size = len(code)
    id = 0
    for i in range(0, size): #convert from higher base back to decimal
        id += alphabet.index(code[i]) * (base ** (size-i-1))
    return id


def is_valid_short(url):
    """Takes in a url and determines if it is a valid shortened url."""
    re_short = re.compile(url_for('main.index') + "[a-kmnp-zA-HJ-NP-Z2-9]+$") #matches our URLs
    return not (not re_short.match(url))


def standardize_url(url):
    """Takes in a url and returns a clean, consistent format. For example:
    example.com, http://example.com, example.com/ all are http://example.com/
    Returns None if the url is somehow invalid."""
    #if is_valid_short(url): #will not shorten one of our already shortened URLs
    #    return None
    parts = parse.urlparse(url, "http") #default scheme is http if omitted
    if parts[0] != "http" and parts[0] != "https": #scheme was not http(s)
        return None

    #url appears valid at this point, proceed with standardization
    standard = parts.geturl()
    #work-around for bug in urlparse
    if standard.startswith("http:///") or standard.startswith("https:///"):
        standard = standard.replace("///", "//", 1) #get rid of extra slash
    if not standard.endswith("/"): #does not end with '/'...
        if re_end.findall(standard): #...but ends with .something...
            if parts[0] == "http":
                bound = 7
            elif parts[0] == "https":
                bound = 8
            if standard.rfind("/", bound) == -1: #...and contains no other '/'
                return standard + "/" #append a '/'
    return standard


def shorten_url(url):
    """Takes in a standard url and returns a shortened version."""
    url = standardize_url(url)
    if url is None: #tried to shorten invalid url
        return None

    #get the id for this url (whether new or otherwise)
    link = Link.query.filter_by(url=url).first()
    if not link: #url not yet inserted into database
        link = Link(url=url)
        db.session.add(link) #insert and get its id
    id = Link.query.filter_by(url=url).first().id
    code = convert_to_code(id)
    return "%s%s" % (url_for('main.index'), code)


def lengthen_url(code):
    """Takes in one of our shortened URLs and returns the correct long url."""
    #isolate code from shortened url
    #if not is_valid_short(url): #url was not constructed properly
    #    return "%s404" % url_for('main.index')

    id = resolve_to_id(code) #convert shortened code to id
    long = Link.query.filter_by(id=id).first()
    if not long: #id was not found in database
        return abort(404)
    return long.url #url to perform 301 re-direct on