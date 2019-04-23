import datetime
from flask import g,request
from . import log_blueprint
from app.models.mysql_sql import memModel,cpuModel,swapModel

from common_utils import json_response

@log_blueprint.route('/select_mem',methods=['POST','GET'])
def select_mem():

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


@log_blueprint.route('/select_cpu',methods=['POST','GET'])
def select_cpu():
    now_time, next_time = dt_range()
    now_time = now_time.strftime("%Y-%m-%d %H") + " 00:00"
    next_time = next_time.strftime("%Y-%m-%d %H") + " 00:00"

    data_tmp = cpuModel.query_hour(now_time, next_time)

    total_data_list = []
    total_time_list = []
    for tmp in data_tmp:
        tmp_list = []
        tmp_list.append(datetime.datetime.strftime(tmp[1], "%H:%M:%S"))
        tmp_list.append(float(tmp[0]))
        total_time_list.append(datetime.datetime.strftime(tmp[1], "%H:%M:%S"))

        total_data_list.append(tmp_list)

    data = {"data_mem": total_data_list, "data_time": total_time_list}
    return json_response(request, status=0, data=data)


@log_blueprint.route('/select_swap',methods=['POST','GET'])
def select_swap():
    now_time, next_time = dt_range()
    now_time = now_time.strftime("%Y-%m-%d %H") + " 00:00"
    next_time = next_time.strftime("%Y-%m-%d %H") + " 00:00"

    data_tmp = swapModel.query_hour(now_time, next_time)

    total_data_list = []
    total_time_list = []
    for tmp in data_tmp:
        tmp_list = []
        tmp_list.append(datetime.datetime.strftime(tmp[1], "%H:%M:%S"))
        tmp_list.append(float(tmp[0]))
        total_time_list.append(datetime.datetime.strftime(tmp[1], "%H:%M:%S"))

        total_data_list.append(tmp_list)

    data = {"data_mem": total_data_list, "data_time": total_time_list}
    return json_response(request, status=0, data=data)




def dt_range():
    now_time = datetime.datetime.now()  # 当前小时的时间
    next_time = now_time + datetime.timedelta(hours=1)  # 下一个小时时间
    return  now_time,next_time