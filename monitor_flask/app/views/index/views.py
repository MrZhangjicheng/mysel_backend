import psutil
from flask import g,request
import datetime
from . import index_blueprint
from common_utils import json_response,bytes_to_gb
import global_data as gol
from app.models.coll_redis.used_redis import get_value



@index_blueprint.route('/cpu',methods=['POST','GET'])
def get_cpu():
    data = dict(
        percent_avg=psutil.cpu_percent(interval=0,percpu=False),
        percent_per = psutil.cpu_percent(interval=0, percpu=True),
        num_p = psutil.cpu_count(logical=False),
        num_l = psutil.cpu_count(logical=True),
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    gol.set_value('cpu',data)
    get_value()
    return json_response(request,data=data,status=0)

@index_blueprint.route('/mem',methods=['POST','GET'])
def get_mem():
    mem_info = psutil.virtual_memory()
    data = dict(
        total = bytes_to_gb(mem_info.total),
        used = bytes_to_gb(mem_info.used),
        free = bytes_to_gb(mem_info.free),
        percent = mem_info.percent,
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    gol.set_value('mem',data)
    get_value()

    return json_response(request,data=data,status=0)


@index_blueprint.route('/swap',methods=['POST','GET'])
def get_swap():
    swap_info = psutil.swap_memory()
    data = dict(
        total =bytes_to_gb(swap_info.total),
        free = bytes_to_gb(swap_info.free),
        used = bytes_to_gb(swap_info.used),
        percent = swap_info.percent,
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    gol.set_value('swap',data)
    get_value()

    return json_response(request,data=data,status=0)


@index_blueprint.route('/disk',methods=['POST','GET'])
def get_disk():
    disk_info = psutil.disk_partitions()
    data = [

        dict(
            device=v.device,
            mountpoint=v.mountpoint,
            fstype=v.fstype,
            opts=v.opts,
            used={
                k: bytes_to_gb(v, k)
                for k, v in psutil.disk_usage(v.mountpoint)._asdict().items()
            }
        )
        for v in disk_info
    ]
    gol.set_value('disk',data)
    get_value()
    return json_response(request,data=data,status=0)

@index_blueprint.route('/net',methods=['POST','GET'])
def get_net():
    net_addrs = psutil.net_if_addrs()
    addrs_info = {
        k: [
            dict(
                family=val.family.name,
                address=val.address,
                netmask=val.netmask,
                broadcast=val.broadcast,

            )
            for val in v if val.family.name == "AF_INET"
        ][0]
        for k, v in net_addrs.items()
    }

    io = psutil.net_io_counters(pernic=True)
    data = [
        dict(
            name=k,
            bytes_sent=v.bytes_sent,
            bytes_recv=v.bytes_recv,
            packets_sent=v.packets_sent,
            packets_recv=v.packets_recv,
            time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **addrs_info[k]
        )
        for k, v in io.items()
    ]
    gol.set_value('net',data)
    get_value()
    return json_response(request,data=data,status=0)