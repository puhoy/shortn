__author__ = 'meatpuppet'


from . import api
from flask import jsonify, url_for, request
from ..shortn.shortn import lengthen_url, shorten_url, _convert_to_code

from ..models.Url import Url



"""
the routes will work if we have the # in the expand function (see main.views)
"""

@api.route('/api/status/', methods=['GET'])
def status():
    """
    just a dummy api function

    :return:
    """
    return jsonify({'status': 'running'})


@api.route('/api/shorten', methods=['PUT'])
def shorten():
    """
    call with a PUT like api/shorten?url=http%3A%2F%2Fstackoverflow.com

    :return:
        returns json:
            {'status': 'ok',
             'code': code,
             's_url': url_for('main.expand', code=code, _external=True),
            }
        or, if something went wrong:
            {'status': 'err'}
    """
    url = request.args.get('url', None)
    if not url:
        return jsonify({'status': 'err'})
    code, long_url = shorten_url(url)
    if not code:
        return jsonify({'status': 'err'})
    return jsonify({'status': 'ok',
                    'code': code,
                    's_url': url_for('main.expand', code=code, _external=True),
                    })


@api.route('/api/expand/<string:code>', methods=['GET'])
def expand(code):
    """
    GET something like api/expand/CODE

    :param code: the short code
    :return:
        {'status': 'ok',
        'url': url}
        or
        {'status': 'err'}
    """
    if code:
        url = lengthen_url(code)
        return jsonify({'status': 'ok',
                        'url': url})
    return jsonify({'status': 'err'})


@api.route('/api/mostclicked', methods=['GET'])
def most_clicked():
    '''
    returns the most clicked links in a json object:
        {
          "items": [
            {
              "clicks": 2,
              "creation_date": "Wed, 06 May 2015 00:08:16 GMT",
              "shorturl": "http://localhost:5000/g",
              "url": "http://sdfa/"
            },
            {
              "clicks": 1,
              "creation_date": "Tue, 05 May 2015 23:47:30 GMT",
              "shorturl": "http://localhost:5000/f",
              "url": "http://cvxbcvb/"
            },
            ...
          ]
        }

    :return:
    '''
    urls = Url.query.order_by(Url.clicks).limit(20)
    ret = []
    for url in urls:
        code = _convert_to_code(url.id)
        ret.append({'url': url.url,
                    'shorturl': url_for('main.expand', code=code, _external=True),
                    'clicks': url.clicks,
                    'creation_date': url.creation_date})
    ret.reverse()
    return jsonify(items=ret)


