import json
import datetime
import time
from sqlalchemy.orm import sessionmaker
from app.models.mysql_sql import mysql_db
from app.object_mysql.models_mysql import Cpu, Mem, Swap
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
    while True:
        time.sleep(300)
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        set_mysql()
        from app.cache.cache_redis import CacheRedis
        cacheRedis = CacheRedis()
        cacheRedis.flushall()
