from django.shortcuts import render
from django.http import Http404
# from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.conf import settings
import json
import os
import time
# Create your views here.
import datetime
from elasticsearch import Elasticsearch, RequestError

es = Elasticsearch('192.168.0.7:9200')



class react_test(APIView):
    def get(self, request, format=None):
        response = {"state": 200}
        return JsonResponse(response, content_type=u"application/json; charset=utf-8")


class create_index(APIView):
    def get(self, request, index_nm, format=None):

        # check es connection status
        if not es.ping():
            print("--- ES Connection failed --")
            raise ValueError("Connection failed")

        # create es index
        if es.indices.exists(index=str(index_nm)):
            print("--- existing index ---", index_nm)

        else:
            try:
                with open('./static/item2item/mapping2.json', 'r') as f:
                    mapping = json.load(f)

                res = es.indices.create(index=index_nm, body=mapping)
            except RequestError as es1:
                print('Index already exists!!', type(es1))

        response = {"state": 200}
        return JsonResponse(response, content_type=u"application/json; charset=utf-8")

class update_index(APIView):

    def get(self, request, index_nm, format=None):
        now = datetime.datetime.now()
        if not es.ping():
            print("--- ES Connection failed --")
            raise ValueError("Connection failed")

        # 데이터 삽입
        doc = {
            '@imestamp': now,
            'value': 'elasticsearch index from python test!!!!'
        }

        try:
            res = es.index(index=index_nm,  doc_type='_doc',  body=doc) #

            response = {"state": res}
        except Exception as e:
            print("error~!!!", e)

        return JsonResponse(response, content_type=u"application/json; charset=utf-8")


class delete_index(APIView):

    def get(self, request, index_nm, format=None):

        now = datetime.datetime.now()

        if not es.ping():
            print("--- ES Connection failed --")
            raise ValueError("Connection failed")

        if es.indices.exists(index=index_nm):
            res = es.indices.delete(index=index_nm)
            response = {"state": 200,
                        "now": now,
                        "index_nm": index_nm,
                        "detail" : res}

        else:
            response = {"state": 400,
                        "now": now,
                        "index_nm": index_nm}


        return JsonResponse(response, content_type=u"application/json; charset=utf-8")


class detail(APIView):

    def get(self, request, question_id, second_key):
        content = {"testing": question_id,
                   "second_key": second_key}

        return JsonResponse(content, content_type=u"application/json; charset=utf-8")

class param1(APIView):
    def get(self, request, format=None):

        # sample 007011000606
        pid = os.getpid()
        content = {"param": pid}

        return JsonResponse(content, content_type=u"application/json; charset=utf-8")



class postman_test(APIView):
    """
    요건 postman에서만 테스트가 가능한놈
    """
    def get(self, request):
        dummy_data = {
            'name': '죠르디',
            'type': '공룡',
            'job': '편의점알바생',
            'age': 5
        }
        return JsonResponse(dummy_data)

    def post(self, request):
        return HttpResponse("post 요청을 잘받았다")

    def put(self, request):
        return HttpResponse("Put 요청을 잘받았다")

    def delete(self, request):
        return HttpResponse("Delete 요청을 잘받았다")

