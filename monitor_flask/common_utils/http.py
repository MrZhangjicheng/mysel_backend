import json
from flask import make_response


def set_headers(response, origin):
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Credentials'] = "true"
    response.headers['Access-Control-Max-Age'] = 1678000
    response.headers['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
    response.headers['Server'] = 'PHP'
    return response


def json_response(req,status,error_msg='',data={},**kwargs):
    m_data={
        'status':status,
        'error_msg':error_msg,
        'data':data
    }
    m_data.update(kwargs)
    m_data =json.dumps(m_data,ensure_ascii=False)
    resp = make_response(m_data)
    resp.headers['Content-Type'] = 'application/json'
    origin =req.headers.get('Origin')
    resp = set_headers(resp,origin)
    return resp