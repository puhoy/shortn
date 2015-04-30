__author__ = 'meatpuppet'

from flask import Blueprint

main = Blueprint('main', __name__,  template_folder='templates', static_folder='static') #Blueprint(moduleName, moduleOrPackage)

from . import views, errors