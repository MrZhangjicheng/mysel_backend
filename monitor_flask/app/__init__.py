
from app.config import ServerConfig
from flask import Flask,request

def init_vendor_odm(app):
    from app.config import MysqlConfig
    from .models.mysql_orm import mysql_db
    app.config.update(
        SQLALCHEMY_DATABASE_URI=MysqlConfig().get_uri())
    mysql_db.init_app(app)



def init_controllers(app):
    from app.views.index import index_blueprint
    app.register_blueprint(index_blueprint, url_prefix='/index')

    from app.views.log import  log_blueprint
    app.register_blueprint(log_blueprint,url_prefix='/log')

    from app.views.test import test_blueprint
    app.register_blueprint(test_blueprint,url_prefix='/test')

    from app.views.time import time_blueprint
    app.register_blueprint(time_blueprint,url_prefix='/time')

def create_app():
    app = Flask(__name__)
    init_vendor_odm(app)
    init_controllers(app)


    return app

def run_app():
    app = create_app()
    app.run(debug=ServerConfig().debug ,host=ServerConfig().host ,port=ServerConfig().port)
