from flask import Blueprint

log_blueprint = Blueprint("log",__name__)
from . import  views