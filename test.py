# check es connection status

import json
import os
import time
# Create your views here.

import datetime
from elasticsearch import Elasticsearch, RequestError
es = Elasticsearch('0.0.0.0:9200')
print("test started!")



if not es.ping():
    print("--- ES Connection failed --")
    raise ValueError("Connection failed")

# create es index
if es.indices.exists(index=str("index_nm")):
    print("--- existing index ---", "index_nm")

else:
    try:
        with open('mapping.json', 'r') as f:
            mapping = json.load(f)

        res = es.indices.create(index="index_nm", body=mapping)
    except RequestError as es1:
        print('Index already exists!!', type(es1))