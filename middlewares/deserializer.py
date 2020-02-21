from flask import jsonify
import json

### converting the dataset from CLient API into JSON
def deserializer(request_obj):
    return request_obj.json()


def binary_to_json(response):
    return json.loads(response.content.decode('utf-8'))