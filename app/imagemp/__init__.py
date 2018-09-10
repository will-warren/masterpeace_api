from flask import Blueprint

imagemp_blueprint = Blueprint('imagemp', __name__)


from . import views