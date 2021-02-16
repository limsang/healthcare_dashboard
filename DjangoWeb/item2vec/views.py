from django.shortcuts import render
from django.http import Http404
# from rest_framework import status
from rest_framework.views import APIView

from django.http.response import JsonResponse
from django.conf import settings
import json
import os
import time
# Create your views here.

class nginx_test(APIView):
    def get(self, request, format=None):

        # sample 007011000606
        pid = os.getpid()
        content = {"testing": pid}

        return JsonResponse(content, content_type=u"application/json; charset=utf-8")

class post_test(APIView):
    def post(self, request, format=None):

        dummy_data = {
            'name': 'aaaaa',
            'type': 'bbbbb',
            'job': request,
            'age': 5
        }

        return JsonResponse(dummy_data, content_type=u"application/json; charset=utf-8")
