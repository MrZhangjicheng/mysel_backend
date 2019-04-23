import datetime
def td(tm):
    dt = datetime.datetime.fromtimestamp(tm)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# 获取日期时间
def dt():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")