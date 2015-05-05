__author__ = 'meatpuppet'


from . import api
from flask import current_app, jsonify, url_for, request
from ..shortn.shortn import lengthen_url, shorten_url, _convert_to_code

from ..models.Url import Url

from sqlalchemy import desc


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


@api.route('/api/shorten', methods=['PUT', 'POST'])
def shorten():  # TODO code aus dem put rausfummeln...
    """

    :return:
    """
    url = request.args.get('url', None)
    if not url:
        return jsonify({'status': 'err'})
    code = shorten_url(url)
    if not code:
        return jsonify({'status': 'err'})
    return jsonify({'status': 'ok',
                    'code': code,
                    's_url': url_for('main.expand', code=code, _external=True),
                    })


@api.route('/api/expand/<code>', methods=['GET'])
def expand(code):
    url = lengthen_url(code)
    return jsonify({'url': url})


@api.route('/api/mostclicked')
def most_clicked():
    '''
    returns the most clicked links

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


