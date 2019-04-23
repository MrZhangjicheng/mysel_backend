import datetime
from flask import g,request
from . import log_blueprint
from app.models.mysql_sql import memModel

from common_utils import json_response

@log_blueprint.route('/select',methods=['POST','GET'])
def select():

    now_time,next_time = dt_range()
    now_time = now_time.strftime("%Y-%m-%d %H") + " 00:00"
    next_time = next_time.strftime("%Y-%m-%d %H") + " 00:00"

    data_tmp = memModel.query_hour(now_time,next_time)

    total_data_list = []
    total_time_list =[]
    for tmp in data_tmp:
        tmp_list = []
        tmp_list.append(datetime.datetime.strftime(tmp[1],"%H:%M:%S"))
        tmp_list.append(float(tmp[0]))
        total_time_list.append(datetime.datetime.strftime(tmp[1],"%H:%M:%S"))

        total_data_list.append(tmp_list)



    data = {"data_mem":total_data_list,"data_time":total_time_list}
    return json_response(request,status=0,data=data)


@log_blueprint.route('/select_three',methods=["POST"])
def select_three():
    id = request.get_json(force=True).get("id")
    now_time,next_time = dt_range()
    now_time = now_time.strftime("%Y-%m-%d ") + "00:00:00"
    next_time = next_time.strftime("%Y-%m-%d ") + "23:59:59"
    data_tmp = memModel.query_three_day(now_time,next_time)
    print(data_tmp)
    total_list = []

    for tmp in data_tmp:
        tmp_list = []
        tmp_list.append(float(tmp[0]))
        tmp_list.append(datetime.datetime.strftime(tmp[1], "%Y-%m-%d %H:%M:%S"))

        total_list.append(tmp_list)

    print(total_list)
    data = {"data": total_list}
    print(data)


@log_blueprint.route('/select_month',methods=["POST"])
def select_month():
    id = request.get_json(force=True).get("id")
    now_time, next_time = dt_range()
    now_time = now_time.strftime("%Y-%m-%d %H") + " 00:00"
    next_time = next_time.strftime("%Y-%m-%d %H") + " 00:00"
    data = memModel.query_three_day(now_time, next_time)
    print(data)




def dt_range():
    now_time = datetime.datetime.now()  # 当前小时的时间
    next_time = now_time + datetime.timedelta(hours=1)  # 下一个小时时间
    return  now_time,next_time