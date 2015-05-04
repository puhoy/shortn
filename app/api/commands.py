__author__ = 'meatpuppet'


from . import api
from flask import current_app, jsonify, url_for, request
from ..main.shorten import lengthen_url, shorten_url

"""
the routes will work if we have the # in the expand function (see main.views)
"""

@api.route('/status/', methods=['GET'])
def status():
    """
    just a dummy api function

    :return:
    """
    return jsonify({'status': 'running'})


@api.route('/shorten', methods=['PUT', 'POST'])
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


@api.route('/e/<code>', methods=['GET'])
def expand(code):
    url = lengthen_url(code)
    return jsonify({'url': url})

