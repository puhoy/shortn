templates__author__ = 'meatpuppet'

from flask import Blueprint

api = Blueprint('api', __name__,  template_folder='templates', static_folder='static') #Blueprint(moduleName, moduleOrPackage)

from . import commands