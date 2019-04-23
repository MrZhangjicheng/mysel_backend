import psutil
import datetime
from flask import g,request
from . import time_blueprint
from .service import td
from common_utils import json_response


@time_blueprint.route('/lastest_start_time',methods=['POST','GET'])
def get_lastest_start_time():
    data = td(psutil.boot_time())
    return json_response(request,data=data,status=0)

@time_blueprint.route('/logined_users',methods=['POST','GET'])
def get_logined_users():
    users = psutil.users()
    data = [
        dict(
            name=v.name,
            terminal=v.terminal,
            host=v.host,
            started=td(v.started),
            pid=v.pid
        )
        for v in users
    ]
    return json_response(request,data=data,status=0)

