
from flask import Blueprint

api = Blueprint('api', __name__)

from app.api_1_0 import woquge




# 查询主表
# @api.route('/<path>', methods=["GET"])
# def api_get(path):
#     print(path)
#     return jsonify()
#
#
# @api.route('/<path>', methods=['POST', 'PUT', 'DELETE'])
# def api_post(path):
#     field = request.get_json().get('field')
#     print(field)
#     # field = 'name'
#     body = {
#         "size": 0,
#         "aggs": {
#             "genres": {
#                 "terms": {"field": field+'.keyword'}
#             }
#         }
#     }
#     try:
#         result = es.search(index='bqg_xiaosh', doc_type="doc", body=body, request_timeout=20)
#     except Exception as e:
#         print(e)
#         return
#     res = result['aggregations']['genres']['buckets']
#     print(res)
#     return jsonify({'code': 0, 'data': res})


