from flask import Blueprint

time_blueprint = Blueprint('time',__name__)

from . import views