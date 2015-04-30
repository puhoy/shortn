__author__ = 'meatpuppet'


from . import api
from flask import current_app, jsonify

@api.route('/status/', methods=['GET'])
def status():
    """
    just a dummy api function

    :return:
    """
    return jsonify({'status': 'running'})

