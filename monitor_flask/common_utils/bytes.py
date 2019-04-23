


def  bytes_to_gb(data,key=''):
    if key == 'percent':
        return data
    else:
        return round(data/(1024 ** 3),2)