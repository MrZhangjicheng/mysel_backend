import json
import datetime
from sqlalchemy.orm import sessionmaker
import global_data as gol
from app.cache.cache_redis import CacheRedis
from app.models.mysql_sql import mysql_db
from app.object_mysql.models_mysql import Cpu, Mem, Swap


def get_value():
    cacheRedis = CacheRedis()
    cpu_info = gol.get_value('cpu')

    mem_info = gol.get_value('mem')
    swap_info = gol.get_value('swap')

    if cpu_info is not None:
        cpu = {
            "percent": cpu_info["percent_avg"],
            "create_date": datetime.datetime.strptime(cpu_info["time"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"),
            "create_time": datetime.datetime.strptime(cpu_info["time"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S"),
            "create_dt": cpu_info["time"]
        }
        cpu_time = cpu_info["time"]
        cpu = json.dumps(cpu)

        cacheRedis.set("cpu " + cpu_time, cpu)

    if mem_info is not None:
        mem = {
            "percent": mem_info["percent"],
            "total": mem_info["total"],
            "used": mem_info["used"],
            "free": mem_info["free"],
            "create_date": datetime.datetime.strptime(mem_info["time"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"),
            "create_time": datetime.datetime.strptime(mem_info["time"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S"),
            "create_dt": mem_info["time"]
        }

        mem_time = mem_info["time"]
        mem = json.dumps(mem)

        cacheRedis.set("mem " + mem_time, mem)

    if swap_info is not None:
        swap = {
            "percent": swap_info["percent"],
            "total": swap_info["total"],
            "used": swap_info["used"],
            "free": swap_info["free"],
            "create_date": datetime.datetime.strptime(swap_info["time"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"),
            "create_time": datetime.datetime.strptime(swap_info["time"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S"),
            "create_dt": swap_info["time"]

        }
        swap_time = swap_info["time"]
        swap = json.dumps(swap)

        cacheRedis.set("swap " + swap_time, swap)


def set_mysql():
    cacheRedis = CacheRedis()
    keys = cacheRedis.get_keys()
    Session = sessionmaker(
        bind=mysql_db,
        autocommit=False,
        autoflush=True,
        expire_on_commit=False

    )
    session = Session()

    for key in keys:
        if "cpu" in str(key):
            cpu_info = json.loads(cacheRedis.get(key))
            cpu = Cpu(
                percent=cpu_info["percent"],
                create_date=cpu_info["create_date"],
                create_time=cpu_info["create_time"],
                create_dt=cpu_info["create_dt"],
            )
            session.add(cpu)
            session.commit()
        if "mem" in str(key):
            mem_info = json.loads(cacheRedis.get(key))
            mem = Mem(
                percent=mem_info['percent'],
                total=mem_info['total'],
                used=mem_info['used'],
                free=mem_info['free'],
                create_date=mem_info["create_date"],
                create_time=mem_info["create_time"],
                create_dt=mem_info["create_dt"]
            )
            session.add(mem)
            session.commit()
        if "swap" in str(key):
            swap_info = json.loads(cacheRedis.get(key))
            swap = Swap(
                percent=swap_info['percent'],
                total=swap_info['total'],
                used=swap_info['used'],
                free=swap_info['free'],
                create_date=swap_info["create_date"],
                create_time=swap_info["create_time"],
                create_dt=swap_info["create_dt"]
            )
            session.add(swap)
            session.commit()


if __name__ == '__main__':
    set_mysql()
    from app.cache.cache_redis import CacheRedis
    cacheRedis = CacheRedis()
    cacheRedis.flushall()


