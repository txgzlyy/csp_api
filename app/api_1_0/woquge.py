from flask import Blueprint, jsonify, request, g
from elasticsearch import Elasticsearch
from . import api

es = Elasticsearch(['http://220.171.100.22:43545'])


@api.route('list', methods=['POST'])
def api_post():
    field = request.get_json().get('field')
    num = request.get_json().get('num', 20)
    print(field)
    body = {
        "size": 0,
        "aggs": {
            "genres": {
                "terms": {"field": field + '.keyword', 'size': num}
            }
        }
    }
    try:
        result = es.search(index='bqg_xiaosh', doc_type="doc", body=body, request_timeout=20)
    except Exception as e:
        print(e)
        return
    print(result)
    res = result['aggregations']['genres']['buckets']
    return jsonify({'code': 0, 'data': res})


@api.route('all_capth', methods=['POST'])
def all_capth():
    name = request.get_json().get('name')
    num = request.get_json().get('num')
    print(num)
    body = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {"name": {"query": name, "operator": "and"}},
                    },
                ]
            }

        },
        "aggs": {
            "genres": {
                "terms": {"field": 'capter.keyword',"size": num,}
            }
        }
    }
    try:
        result = es.search(index='bqg_xiaosh', doc_type="doc", body=body, request_timeout=20)
    except Exception as e:
        print(e)
        return
    res = result['aggregations']['genres']['buckets']
    return jsonify({'code': 0, 'data': res})


@api.route('capter_infos', methods=['POST'])
def capth_infos():
    capter = request.get_json().get('capter')
    name = request.get_json().get('name')
    print(capter)
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {"name": {"query": name, "operator": "and"}},
                    },
                    {
                        "match": {"capter": {"query": capter, "operator": "and"}},
                    },
                ]
            }

        }
    }
    try:
        result = es.search(index='bqg_xiaosh', doc_type="doc", body=body, request_timeout=20)
    except Exception as e:
        print(e)
        return
    res = result['hits']['hits']
    return jsonify({'code': 0, 'data': res})