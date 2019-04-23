import os
import sqlalchemy
from app.config import MysqlConfig
sql_path = os.path.abspath(os.path.dirname(__file__))

mysql_db = sqlalchemy.create_engine(MysqlConfig().get_uri(),encoding="utf8")


from .mem import MemModel
from .cpu import CpuModel
from .swap import SwapModel
memModel = MemModel()
cpuModel = CpuModel()
swapModel = SwapModel()

