import json
import numpy as np
from flask import Flask, request, jsonify
from flasgger import Swagger, fields
from flasgger.utils import swag_from
from flasgger import LazyString, LazyJSONEncoder
import random
import sys

def add_2_numbers(num1, num2):
    output = {"sum_of_numbers": 0}
    sum_of_2_numbers = num1 + num2
    output["sum_of_numbers"] = sum_of_2_numbers
    return output

def get_code_name_list():
    data = load_item_code_name()
    try:
        map = dict()
        for idx, item in enumerate(data):

            map[item] = data[item]
        output = {"data": map}

    except Exception as e:
        print("get_code_name_list", e)
    return output

def get_i2i_rec_list(cemprdcd, rec_list, check):
    if check:
        output = {"target_cemprdcd": cemprdcd}
        output["target_name"] = rec_list['target_item']
        output["rec_items_cd"] = rec_list['rec_items_cd']
        output["rec_items"] = rec_list['rec_items']
        output["len"] = len(rec_list['rec_items'])
        output["check"] = True

    else:
        output = {"target_cemprdcd": cemprdcd}
        output["target_name"] = None
        output["rec_items_cd"] = None
        output["rec_items"] = None
        output["len"] = 0
        output["check"] = False
    return output


app = Flask(__name__)
app.config["SWAGGER"] = {"title": "Swagger-UI", "uiversion": 2}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/swagger/",
}

template = dict(
    swaggerUiPrefix=LazyString(lambda: request.environ.get("HTTP_X_SCRIPT_NAME", ""))
)

app.json_encoder = LazyJSONEncoder
swagger = Swagger(app, config=swagger_config, template=template)
# Swagger(app)
@app.route("/")
def index():
    return "Amore recsys REST API"

@app.route("/상품명 & 코드", methods=["GET"])
@swag_from("swagger_config/swagger_config.yml")
def show_info():
    try:
        # res = load_item_code_name
        res = get_code_name_list()
    except Exception as e:
        print("show_info", e)

    return json.dumps(res, ensure_ascii=False)


@app.route('/personalize_recsys/<string:comcsno>/', methods=['GET'])
@swag_from("swagger_config/personalize_rec.yml")
def personalize(comcsno):
    output = {"success": False}
    output["message"] = "준비중입니다..."
    return json.dumps(output, ensure_ascii=False)

    # api.abort(404, "{} doesn't exist".format(id))

@app.route('/item2item_recsys/<string:cemprdcd>/', methods=['GET'])
@swag_from("swagger_config/item2item.yml")
def item2item(cemprdcd):
    try:
        '''cemprdcd -> rec'''
        # sample 007011000606
        input_json = request.get_json()
        data = load_json_data(cemprdcd)

        if isinstance(data, dict):
            res = get_i2i_rec_list(cemprdcd, data, True)
            return json.dumps(res, ensure_ascii=False)

        else:
            res = get_i2i_rec_list(cemprdcd, data, False)
            return json.dumps(res, ensure_ascii=False)

    except Exception as e:
        print('GoodsListManager', e)


def load_json_data(cemprdcd):
    with open("item_info.json", 'r') as f:
        json_data = json.load(f)
        try:
            return (json_data[cemprdcd])

        except KeyError as e:
            print('상품정보 없음', e)
            return -1

def load_item_code_name():
    with open("code_name.json", 'r') as f:
        json_data = json.load(f)
        try:
            return json_data

        except KeyError as e:
            print('상품정보 없음', e)
            return -1

if __name__ == "__main__":
    # get_code_name_list()
    app.run(host="0.0.0.0", debug=True, port=8080)
