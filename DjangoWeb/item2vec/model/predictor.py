import os 
import numpy as np 
import flask
import tarfile, boto3
import json

from flask import Flask, request
from config.config import config

#BUCKET_NAME = config().json_data["ML_Flow"]["BUCKET_NAME"]
#ARTIFACT_PATH =  config().json_data["ML_Flow"]["ARTIFACT_PATH"]  # path S3 Bucket

def get_api_server():
    app = Flask(__name__)
 
    @app.route('/ping', methods=['GET'])
    def ping():
        """ Sagemaker Health Check...loading is okay?"""
        return flask.Response(response='\n', status=200, mimetype='application/json')

    @app.route('/invocations', methods=['POST'])
    def get_personal_recommendation():
        
        """웹페이지에서 입력받은 UserId가 들어온다."""
        content = request.json

        userId = content['userId']

        try:    

            if userId is None:
                response = {
                    'code': "0001",
                    'message': 'put user id'
                }
                result = json.dumps(response)
                return flask.Response(response=result, status=200, mimetype='application/json')

            else:

                if userId == "null":
                    response = {
                        'code': "0002",
                        'message': 'user id is null'
                    }
                    result = json.dumps(response)
                    return flask.Response(response=result, status=200, mimetype='application/json')

                response = {
                    'code': "0000",
                    'userId': userId,
                    'history_items_info': "items_info",
                    'recommendation_items_info': "recommendation_items_info"
                }
                dump_response = json.dumps(response)

                return flask.Response(response=dump_response, status=200, mimetype='applicaton/json')
        except Exception as e:
            dump_exception = json.dumps(e)
            return flask.Response(response=dump_exception, status=500, mimetype='appication/json')

    return app

def serve():
    # WAS
    api_server = get_api_server()
    return api_server

app = serve()