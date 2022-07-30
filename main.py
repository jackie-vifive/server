from flask import Flask, Response, request
from flask_cors import CORS
import json
from datetime import datetime

import rest_utils
import pandas as pd



app = Flask(__name__)
CORS(app)

##################################################################################################################

# This path simply echoes to check that the app is working.
# The path is /health and the only method is GETs
@app.route("/health", methods=["GET"])
def health_check():
    rsp_data = {"status": "healthy", "time": str(datetime.now())}
    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="application/json")
    return rsp


# The method take any REST request, and produces a response indicating what
# the parameters, headers, etc. are.
@app.route("/api/demo/<parameter1>", methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/api/demo/", methods=["GET", "POST", "PUT", "DELETE"])
def demo(parameter1=None):
    """
    Returns a JSON object containing a description of the received request.

    :param parameter1: The first path parameter.
    :return: JSON document containing information about the request.
    """
    inputs = rest_utils.RESTContext(request, {"parameter1": parameter1})
    data = inputs.data
    data = data[0]

    df = pd.DataFrame(data, index=[0])
    df.loc[0, 'config'] = df.loc[0, 'config'].strip('[]').split(',')
    df.loc[0, 'filter_tags'] = df.loc[0, 'filter_tags'].strip('[]').split(',')
    df.to_csv('new_exercise.csv')

    msg = {
        "/demo received the following inputs": inputs.to_json()
    }
    print("/api/demo/<parameter> received/returned:\n", msg)

    rsp = Response(json.dumps(msg), status=200, content_type="application/json")
    return rsp

##################################################################################################################

@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003)
