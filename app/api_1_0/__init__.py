import re, json, requests


from flask import Blueprint, jsonify, request, g

from nameko.standalone.rpc import ClusterRpcProxy


import time

api = Blueprint('api', __name__)

try:
    from app.api_1_0 import file_controller
except Exception as e:
    print(e)


# 查询主表
@api.route('/<path>', methods=["GET"])
def api_get(path):
    print(path)
    return jsonify()


@api.route('/<path>', methods=['POST', 'PUT', 'DELETE'])
def api_post(path):
    print(request.get_json())
    return jsonify({'data':'OK'})



